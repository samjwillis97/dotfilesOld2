" COLORS
syntax enable
set t_Co=256
let base16colorspace=256
set bg=dark

" UI CONFIG
set number
set showcmd
set cursorline
filetype indent on
set wildmenu
set lazyredraw
set showmatch
set encoding=utf-8
set nocompatible

" SWAP FILE MANAGEMENT
set swapfile
set dir=/tmp

" MAKE NUMBERING RELATIVE
set number
set relativenumber

" SUDO FILES
command! -nargs=0 Sw w !sudo tee % > /dev/null

" SEARCHING
set incsearch
set hlsearch
nnoremap <leader><space> :nohlsearch<CR>

" FOLDING
set foldenable
set foldlevelstart=10
set foldnestmax=10
nnoremap <space> za
set foldmethod=indent

" MOVEMENT
nnoremap j gj
nnoremap k gk

" SPLIT NAVIGATIONS
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

set splitbelow
set splitright


" reopening a file
if has("autocmd")
	au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif 
endif

" DEFAULT FILES
" set backspace=2
set backspace=indent,eol,start
set tabstop=4
set softtabstop=4
set shiftwidth=4
set smarttab

" FZF SEARCH
" Requires silver search and bat
let $FZF_DEFAULT_COMMAND = 'ag --hidden --ignore .git -g ""'
let $FZF_DEFAULT_OPTS = "--preview 'bat --theme Dracula --color=always --style=header,grid --line-range :300 {}'"
let g:fzf_preview_window = ['right:50%', 'ctrl-/']
let g:fzf_layout = { 'window': { 'width': 0.9, 'height': 0.6  } }
let g:fzf_colors =
\ { 'fg':      ['fg', 'Normal'],
  \ 'bg':      ['bg', 'Normal'],
  \ 'hl':      ['fg', 'Comment'],
  \ 'fg+':     ['fg', 'CursorLine', 'CursorColumn', 'Normal'],
  \ 'bg+':     ['bg', 'CursorLine', 'CursorColumn'],
  \ 'hl+':     ['fg', 'Statement'],
  \ 'info':    ['bg', 'PreProc'],
  \ 'border':  ['fg', 'Keyword'],
  \ 'prompt':  ['fg', 'Conditional'],
  \ 'pointer': ['fg', 'Exception'],
  \ 'marker':  ['fg', 'Keyword'],
  \ 'spinner': ['fg', 'Label'],
  \ 'header':  ['fg', 'Comment'] }

nnoremap <leader>f :Files<CR>
nnoremap <leader>F :Rg<CR>
nnoremap <leader>b :Buffers<CR>

" ALE
nmap <silent> ]e <Plug>(ale_next_wrap)
nmap <silent> [e <Plug>(ale_previous_wrap)

" NERD TREE
nnoremap <C-n> :NERDTreeToggle<CR>
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
let NERDTreeIgnore = [ '__pycache__', '\.pyc$', '\.o$', '\.swp',  '*\.swp',  'node_modules/' ]
let NERDTreeShowHidden=1
let NERDTreeChDirMode=2

set laststatus=2

function! s:check_back_space() abort
    let col = col('.') - 1
    return !col || getline('.')[col - 1]  =~# '\s'
endfunction

"" VIM-PLUGINS

" Install vim-plug if not found
if empty(glob('~/.vim/autoload/plug.vim'))
    silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
      \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

" Run PlugInstall if there are missing plugins
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
    \| PlugInstall --sync | source $MYVIMRC
\| endif"

" Plug.vim
call plug#begin('~/.vim/plugged')

" Ale
" Plug 'dense-analysis/ale'
" AutoComplete
Plug 'neoclide/coc.nvim', {'branch': 'release'}
" File Browser
Plug 'preservim/nerdtree'
" Git Plugin for NerdTree
Plug 'Xuyuanp/nerdtree-git-plugin'
" Auto-pairing brackets
Plug 'jiangmiao/auto-pairs'
" Shows git diff in the gutter column
Plug 'airblade/vim-gitgutter'
" Git Plugin
Plug 'tpope/vim-fugitive'
" Easier and better commenting
Plug 'tpope/vim-commentary'
" Airline
Plug 'vim-airline/vim-airline'
" FZF Search
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
" Collection of language packs (syntax, indent etc)
Plug 'sheerun/vim-polyglot'
" Dracula Colorscheme
Plug 'dracula/vim', {'as':'dracula'}
" Arduino
Plug 'stevearc/vim-arduino'
call plug#end()

colorscheme dracula
