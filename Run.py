from string import Template
import os

# ==============================

settings = {
    'bashrcPath': os.path.expanduser('~/.bashrc'),
    'vimrcPath': os.path.expanduser('~/.vimrc'),
    'vimPath': os.path.expanduser('~/.vim'),
    'docsPaths': {
        'c': '/mnt/c',
        'd': '/mnt/d',
        'desktop': '/mnt/c/Users/95phm/Desktop'
    },
    'sshServers': {}
}

# ==============================


class MyTemplate(Template):
    delimiter = '@'


def generateDocsAlias(name, path):
    return MyTemplate(
        '''    elif [ "$1" == "@name" ]; then
        run_docs "@path"'''
    ).substitute(name=name, path=path)


bashrc = MyTemplate('''run_docs() {
    if [ $# -eq 0 ]; then
        run_docs .
    elif [ "$1" == "snapshot" ]; then
        SNAPSHOTDIR="$(head -n 1 ~/snapshotdata)"
        run_docs "$SNAPSHOTDIR"
@docsAlias
    elif [ -d "$1" ]; then
        cd "$1"
        clear
        echo "[$1]"
        ls -A --color=auto
    else
        echo "Such directory doesn't exist!"
    fi
}

run_snapshot() {
    echo "$PWD" > ~/snapshotdata
    echo "Took a snapshot of the current directory!"
}

alias reload="exec bash"
alias ls="ls -A --color=auto"
alias docs=run_docs
alias snapshot=run_snapshot
alias cmd="cmd.exe"
alias cat="python3 -m pygments"
''').substitute(
    docsAlias='\n'.join(generateDocsAlias(name, path)
                        for name, path in settings['docsPaths'].items())
)

print('Generated bashrc:')
print(bashrc)

shouldWriteBashrc = input(
    'Write it on %s? (\'y\': Yes): ' % settings['bashrcPath']
).strip()

if shouldWriteBashrc == 'y':
    with open(settings['bashrcPath'], 'w') as p:
        p.write(bashrc)
        print('Wrote bashrc to %s\n' % settings['bashrcPath'])

vimrc = MyTemplate('''set nocompatible
set backspace=indent,eol,start

syntax on
filetype off

set rtp+=@vimPath/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'ntpeters/vim-better-whitespace'
Plugin 'patstockwell/vim-monokai-tasty'
Plugin 'udalov/kotlin-vim'
call vundle#end()

filetype plugin indent on

set expandtab
set tabstop=4
set softtabstop=4
set shiftwidth=4
set report=0
set colorcolumn=80
set tw=0
set number

colorscheme default
''').substitute(vimPath=settings['vimPath'])

print('Generated vimrc:')
print(vimrc)
shouldWriteVimrc = input(
    'Write it on %s? (\'y\': Yes): ' % settings['vimrcPath']).strip()

if shouldWriteVimrc == 'y':
    with open(settings['vimrcPath'], 'w') as p:
        p.write(vimrc)
        print('Wrote vimrc to %s\n' % settings['vimrcPath'])

shouldInstallVundle = input(
    'Install Vundle for vim on %s? (\'y\': Yes): ' % settings['vimPath']
).strip()

if shouldInstallVundle == 'y':
    os.system(
        'git clone https://github.com/VundleVim/Vundle.vim.git %s/bundle/Vundle.vim' %
        settings['vimPath']
    )

    print('Installed Vundle\n')

print('Done!')
