import os, json, subprocess, shutil

DRY_RUN=False
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

def rsync(src, dst, exclude=None, delete=False, shallow=False, **kwargs):
    cmd = [shutil.which('rsync'), '--verbose', '--times', '--compress', '--progress']
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
    print(' '.join(cmd))
    return subprocess.run(cmd, **kwargs).returncode
