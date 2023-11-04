import argparse, shlex, os, json, subprocess, shutil

DRY_RUN=False
exclude_sync = [
    '.hg',
    '.git',
    '*build/',
    'build*/',
    '.tox',
    '*.deb',
    '*.rpm',
    "*.a1",
    "*.a2",
    "*.a4",
    "*.a5",
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.gif",
    "*.ttf",
    "*.tga",
    "*.dds",
    "*.ico",
    "*.eot",
    "*.pdf",
    "*.swf",
    "*.jar",
    "*.zip",
    "*.dll",
    "*.obj",
    "*.o",
    "*.a",
    "*.lib",
    "*.so",
    "*.so.*",
    "*.dylib",
    "*.onnx",
    '.cache/'
]
remote_dir = os.path.expanduser('~/remote')

def get_mounts():
    mounts_path = os.path.expanduser('~/.mounts.json')
    if os.path.exists(mounts_path):
        with open(mounts_path) as f:
            return json.load(f)
    return {}

mounts = get_mounts()
def get_local_path(host, path):
    if host in mounts:
        m = mounts[host]
        local = m[0]
        remote = m[1]
        return path.replace(remote, local)
    return os.path.join(remote_dir, host, path[1:])

def get_remote_path(host, path):
    p = os.path.abspath(path)
    if host in mounts:
        m = mounts[host]
        local = m[0]
        remote = m[1]
        return p.replace(local, remote)
    return p.replace(os.path.join(remote_dir, host), '')

def get_remote_host(path):
    p = os.path.abspath(path)
    if p.startswith(remote_dir):
        x = p.split('/')
        return x[x.index('remote')+1]
    for host in mounts:
        m = mounts[host]
        local = m[0]
        if p.startswith(local):
            return host
    return None

def get_path_map(host):
    if host in mounts:
        return [mounts[host]]
    # clangd usually doesnt handle using the root / directory
    paths = ['/home', '/usr', '/opt']
    return [[get_local_path(host, path), path] for path in paths]


def needs_sync(host):
    return host and not host in mounts

def add_trail_slash(s):
    if not s.endswith('/'):
        return s + '/'
    return s

def remove_trail_slash(s):
    if s.endswith('/'):
        return s[:-1]
    return s

def remote_isdir(host, path):
    return subprocess.run(['ssh', host, 'test -d {}'.format(shlex.quote(path))]).returncode == 0

def pipe_writeline(pipe, s):
    if pipe:
        pipe.write((s + "\n").encode('utf-8'))

def rsync(src, dst, exclude=None, delete=False, shallow=False, quiet=False, **kwargs):
    cmd = [shutil.which('rsync'), '--times', '--compress']
    if quiet:
        cmd.append('--quiet')
    else:
        cmd.append('--verbose')
        cmd.append('--progress')
    if DRY_RUN:
        cmd.append('--dry-run')
    if delete:
        cmd.append('--delete')
        cmd.append('--delete-excluded')
    if shallow:
        cmd.append('--dirs')
    else:
        cmd.append('--recursive')
    for e in exclude or []:
        cmd.append('--exclude')
        cmd.append(e)
    isdir = os.path.isdir(src if ':' in dst else dst)
    if isdir:
        cmd.append(add_trail_slash(src))
        cmd.append(remove_trail_slash(dst))
    else:
        cmd.append(src)
        cmd.append(dst)
    # print(' '.join(cmd))
    return subprocess.run(cmd, **kwargs).returncode

def remote_sync(args, f, pipe=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to sync with remote')
    parser.add_argument('--delete', '-d', action='store_true', help='delete files missing')
    parser.add_argument('--all', '-a', action='store_true', help='dont exclude any files')
    parser.add_argument('--quiet', '-q', action='store_true', help='Less output')
    parser.add_argument('--shallow', '-s', action='store_true', help='only sync current directory')
    pargs = parser.parse_args(args)
    local = pargs.file or os.getcwd()
    host = get_remote_host(local)
    if host in mounts:
        return 0
    remote_path = get_remote_path(host, local)
    remote = '{}:{}'.format(host, remote_path)
    # Make sure local directory exists
    if not os.path.exists(local):
        if remote_isdir(host, remote_path):
            os.makedirs(local)
        elif not os.path.exists(os.path.dirname(local)):
            os.makedirs(os.path.dirname(local))
    src, dst = f(local, remote)
    exclude = not pargs.all if os.path.isdir(local) else False
    return rsync(src, dst, exclude=exclude_sync if exclude else [], delete=pargs.delete, shallow=pargs.shallow, quiet=pargs.quiet, stdout=pipe, stderr=subprocess.STDOUT)

def pull(args, pipe=None):
    return remote_sync(args, lambda local, remote: (remote, local), pipe=pipe)

def push(args, pipe=None):
    return remote_sync(args, lambda local, remote: (local, remote), pipe=pipe)
