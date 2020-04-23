import argparse
import sys
import os
import os.path as osp
import glob
from pipes import quote
from multiprocessing import Pool, current_process
import shutil

import mmcv

def dump_frames(vid_item):
    full_path, vid_path, vid_id = vid_item
    vid_name = vid_path.split('.')[0]


    if args.temp_dir is None:
        temp_dir = args.out_dir
    else:
        temp_dir = args.temp_dir
        try:
            os.mkdir(osp.join(args.temp_dir, vid_name))
        except OSError:
            pass

    try:
        os.mkdir(osp.join(args.out_dir, vid_name))
    except OSError:
        pass
    vr = mmcv.VideoReader(full_path)
    video_length = 0
    while vr.vcap.isOpened():
        ret, frame = vr.vcap.read()
        if ret:
            if arg.temp_dir is not None:
                mmcv.imwrite(frame, '{}/img_{:05d}.jpg'.format(osp.join(args.temp_dir, vid_name), video_length + 1))
            else:
                mmcv.imwrite(frame, '{}/img_{:05d}.jpg'.format(osp.join(args.out_dir, vid_name), video_length + 1))
        else:
            break
        video_length += 1
    print('{} done with {} frames'.format(vid_name, video_length))
    sys.stdout.flush()
    vr.vcap.release()

    if args.temp_dir is not None:
        shutil.move(osp.join(args.temp_dir, vid_name), osp.join(args.out_dir, vid_name))
    return True


def run_optical_flow(vid_item, dev_id=0):
    full_path, vid_path, vid_id = vid_item
    vid_name = vid_path.split('.')[0]
    out_full_path = osp.join(args.out_dir, vid_name)
    try:
        os.mkdir(out_full_path)
    except OSError:
        pass

    current = current_process()
    dev_id = (int(current._identity[0]) - 1) % args.num_gpu
    image_path = '{}/img'.format(out_full_path)
    flow_x_path = '{}/flow_x'.format(out_full_path)
    flow_y_path = '{}/flow_y'.format(out_full_path)

    cmd = osp.join(args.df_path + 'build/extract_warp_gpu') + \
        ' -f={} -x={} -y={} -b=20 -t=1 -d={} -s=1 -o={}'.format(
            quote(full_path), quote(flow_x_path), quote(flow_y_path),
            dev_id, args.out_format)

    os.system(cmd)
    print('warp on {} {} done'.format(vid_id, vid_name))
    sys.stdout.flush()
    return True


def parse_args():
    parser = argparse.ArgumentParser(description='extract optical flows')
    parser.add_argument('src_dir', type=str)
    parser.add_argument('out_dir', type=str)
    parser.add_argument('temp_dir', type=str, default=None)
    parser.add_argument('--level', type=int,
                        choices=[1, 2],
                        default=2)
    parser.add_argument('--num_worker', type=int, default=8)
    parser.add_argument('--flow_type', type=str,
                        default=None, choices=[None, 'tvl1', 'warp_tvl1'])
    parser.add_argument('--df_path', type=str,
                        default='../../mmaction/third_party/dense_flow')
    parser.add_argument("--out_format", type=str, default='dir',
                        choices=['dir', 'zip'], help='output format')
    parser.add_argument("--ext", type=str, default='avi',
                        choices=['avi', 'mp4', 'webm'], help='video file extensions')
    parser.add_argument("--new_width", type=int, default=0,
                        help='resize image width')
    parser.add_argument("--new_height", type=int,
                        default=0, help='resize image height')
    parser.add_argument("--num_gpu", type=int, default=8, help='number of GPU')
    parser.add_argument("--resume", action='store_true', default=False,
                        help='resume optical flow extraction '
                        'instead of overwriting')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    if args.temp_dir is None:
        temp_dir = args.out_dir
    else:
        temp_dir = args.temp_dir

    if not osp.isdir(temp_dir):
        print('Creating folder: {}'.format(temp_dir))

    if not osp.isdir(args.out_dir):
        print('Creating folder: {}'.format(args.out_dir))

        os.makedirs(args.out_dir)
    if args.level == 2:
        classes = os.listdir(args.src_dir)
        for classname in classes:
            new_out_dir = osp.join(args.out_dir, classname)
            new_temp_dir = osp.join(temp_dir, classname)

            if not osp.isdir(new_out_dir):
                print('Creating folder: {}'.format(new_out_dir))
                os.makedirs(new_out_dir)

            if not osp.isdir(new_temp_dir):
                print('Creating folder: {}'.format(new_temp_dir))
                os.makedirs(new_temp_dir)

    print('Reading videos from folder: ', args.src_dir)
    print('Extension of videos: ', args.ext)
    if args.level == 2:
        fullpath_list = glob.glob(args.src_dir + '/*/*.' + args.ext)
        done_fullpath_list = glob.glob(args.out_dir + '/*/*')
        done_temppath_list = glob.glob(temp_dir + '/*/*')

    elif args.level == 1:
        fullpath_list = glob.glob(args.src_dir + '/*.' + args.ext)
        done_fullpath_list = glob.glob(args.out_dir + '/*')
    print('Total number of videos found: ', len(fullpath_list))
    if args.resume:
        fullpath_list = set(fullpath_list).difference(set(done_fullpath_list))
        fullpath_list = list(fullpath_list)
        print('Resuming. number of videos to be done: ', len(fullpath_list))


    if args.level == 2:
        vid_list = list(map(lambda p: osp.join(
            '/'.join(p.split('/')[-2:])), fullpath_list))
    elif args.level == 1:
        vid_list = list(map(lambda p: p.split('/')[-1], fullpath_list))

    pool = Pool(args.num_worker)
    if args.flow_type == 'tvl1':
        pool.map(run_optical_flow, zip(
            fullpath_list, vid_list, range(len(vid_list))))
    elif args.flow_type == 'warp_tvl1':
        pool.map(run_warp_optical_flow, zip(
            fullpath_list, vid_list, range(len(vid_list))))
    else:
        pool.map(dump_frames, zip(
            fullpath_list, vid_list, range(len(vid_list))))
