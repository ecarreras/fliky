import sys
import os

class GitError(Exception):
    pass

def git(*args):
    import subprocess
    cmd = subprocess.Popen(['git'] + list(args),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        cwd='/Users/eduard/Desktop/fliky')
    print ' '.join(['git'] + list(args))
    return cmd

def gitq(*args):
    cmd = git(*args)
    stdout, stderr = cmd.communicate()
    print stdout, stderr
    return cmd.returncode

def git_commit(msg, author):
    # See if we have something to commit; if not, just return
    gitq('update-index', '--refresh')
    r = gitq('diff-index', '--exit-code', '--quiet', 'HEAD')
    if r == 0:
        return
        
    r = gitq('commit', '-m', msg, '--author', author)
    
    if r != 0:
        raise GitError, r

def git_log(file = None, files = None):
    if not files:
        files = []
    if file:
        files.append(file)
    
    cmd = git("rev-list", "--all", "--pretty=raw",  "HEAD", "--", *files)
    cmd.stdin.close()
    
    content = cmd.stdout.read()
    cmd.wait()
    
    if cmd.returncode != 0:
        GitError, cmd.returncode
    
    content = content.replace("\n    ", "message ")
    content = content.split('\n\n')[:-1]
    commits = []
    for block in content:
        commit = {}
        lines = block.split("\n")
        for line in lines:
            key, value = line.split(' ', 1)
            commit[key] = value
        git_commit_fmt(commit)
        commits.append(commit)
    
    return commits
    
def git_add(*files):
    r = gitq('add', "--", *files)
    if r != 0:
        raise GitError, r

def git_remove(*files):
    r = gitq('rm', '-f', '--', *files)
    if r != 0:
        raise GitError, r

def git_show(file_cid):
    cmd = git("show", "--pretty=raw", file_cid)
    content = cmd.stdout.read()
    cmd.wait()
    return content

def git_commit_log(cid):
    cmd = git("rev-list", "-n1", "--pretty=raw", cid)
    out = cmd.stdout.read()
    cmd.wait()
    out = out.replace("\n    ", "message ")
    commit = {}
    for l in out.split('\n'):
        l = l.strip()
        if l:
            key, value = l.split(' ', 1)
            commit[key] = value
    git_commit_fmt(commit)
    return commit

def git_diff(name, cid1, cid2):
    cmd = git("diff", cid1 + ".." + cid2, name)
    out = cmd.stdout.read()
    cmd.wait()
    return out

def git_commit_fmt(commit):
    if 'author' in commit:
        author, epoch, tz = commit['author'].rsplit(' ', 2)
        epoch = float(epoch)
        author, email = author.rsplit(' <', 1)
        commit['author'] = author
        commit['aemail'] = email[:-1]
        commit['atime'] = datetime.datetime.fromtimestamp(epoch)
    
    if 'committer' in commit:
        committer, epoch, tz = commit['committer'].rsplit(' ', 2)
        epoch = float(epoch)
        committer, email = committer.rsplit(' <', 1)
        commit['committer'] = committer
        commit['cemail'] = email[:-1]
        commit['ctime'] = datetime.datetime.fromtimestamp(epoch)

def git_init(git_dir):
    gitq("init", git_dir)

