call plug#begin()
	" Syntax
	Plug 'sheerun/vim-polyglot'
	Plug 'jiangmiao/auto-pairs'
	Plug 'tpope/vim-surround'
	Plug 'tomtom/tcomment_vim'
	" File Explorer
	Plug 'scrooloose/NERDTree'
	Plug 'ryanoasis/vim-devicons'
	" Rich Presence
	" Plug 'vimsence/vimsence'
    " Git
    Plug 'tpope/vim-fugitive'
	" Theme
    Plug 'bluz71/vim-moonfly-colors'
    Plug 'NLKNguyen/papercolor-theme'
	Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'
    Plug 'chrisbra/Colorizer'
    Plug 'mhinz/vim-startify'
	" CoC
	" Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " VimWiki
    Plug 'vimwiki/vimwiki'
    " fzf
	Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'
call plug#end()

" Change cursor shape in different modes
if &term =~ "screen."
    let &t_ti.="\eP\e[1 q\e\\"
    let &t_SI.="\eP\e[5 q\e\\"
    let &t_EI.="\eP\e[1 q\e\\"
    let &t_te.="\eP\e[0 q\e\\"
else
    let &t_ti.="\<Esc>[1 q"
    let &t_SI.="\<Esc>[5 q"
    let &t_EI.="\<Esc>[1 q"
    let &t_te.="\<Esc>[0 q"
endif

" General Settings
syntax on
filetype plugin on
set nocompatible
set clipboard=unnamedplus
set number relativenumber
set tabstop=4 softtabstop=4
set shiftwidth=4
" set termguicolors
set smartindent
set expandtab
set cmdheight=1
set background=dark
set ignorecase
set smartcase
set noswapfile
set splitbelow
set splitright
set incsearch
set autowrite
set noendofline
set nofixendofline
set mouse=a

" Theme
colo ThemerVim

let g:airline_theme='behelit'
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail_improved'
set showtabline=2
set laststatus=2
set noshowmode

" Startify
autocmd VimEnter *
            \   if !argc()
            \ |   Startify
            \ |   set number relativenumber
            \ | endif

" VimWiki
let g:vimwiki_list = [{'path': '~/.wiki/',
                      \ 'syntax': 'markdown', 'ext': '.md'}]

" Mappings
let mapleader=' '
nnoremap \ :noh<return>
:map<C-n>    :NERDTree<CR>
nnoremap <C-p> :Files<Cr>
nmap <F2> <Plug>(coc-rename)
autocmd filetype cpp nnoremap <buffer> <C-c> :!g++ -std=c++14 -Wshadow -Wall -o %:t:r % -g -fsanitize=address -fsanitize=undefined -D_GLIBCXX_DEBUG && ./%:t:r<CR>
autocmd filetype python nnoremap <buffer> <C-c> :!python3 %<CR>