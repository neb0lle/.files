call plug#begin()
" Syntax:
	Plug 'sheerun/vim-polyglot'
	Plug 'jiangmiao/auto-pairs'
	Plug 'tpope/vim-surround'
	Plug 'tpope/vim-commentary'
	Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
" Version Control:
	Plug 'tpope/vim-fugitive'
" Theme:
	Plug 'lukas-reineke/indent-blankline.nvim'
	Plug 'ryanoasis/vim-devicons'
	Plug 'vim-airline/vim-airline'
	Plug 'vim-airline/vim-airline-themes'
	Plug 'norcalli/nvim-colorizer.lua'
	Plug 'glepnir/dashboard-nvim'
" CoC:
	" Plug 'neoclide/coc.nvim', {'branch': 'release'}
" VimWiki:
    Plug 'vimwiki/vimwiki'
" FZF:
	Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
	Plug 'junegunn/fzf.vim'
" Misc:
	Plug 'christoomey/vim-tmux-navigator'
	Plug 'ThePrimeagen/vim-be-good'
call plug#end()

"	General Settings:
syntax on
filetype plugin indent on
set nocompatible
set number relativenumber
set nohlsearch
set hidden
set noerrorbells
set nowrap
set smartcase
set ignorecase
set incsearch

set noswapfile
set nobackup
set undofile
set clipboard=unnamedplus

set splitbelow
set splitright
set autowrite
set noendofline
set nofixendofline
set autoread

set smartindent
set autoindent
set smarttab
set noexpandtab
set tabstop=4 
set shiftwidth=4
set softtabstop=4
set scrolloff=8

"	Theme:
colorscheme ThemerVim
set background=dark
highlight Normal guibg=None
set cmdheight=1
set showtabline=2
set laststatus=2
set noshowmode
" set termguicolors
" set colorcolumn=80

let g:airline_theme='behelit'
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail_improved'

"	Treesetter:
lua <<EOF
require'nvim-treesitter.configs'.setup {
  highlight = {
    enable = true,
    additional_vim_regex_highlighting = false,
  },
}
EOF

"	Dashboard:
highlight dashboardHeader ctermfg=8 cterm=bold
highlight dashboardCenter ctermfg=12
let g:dashboard_default_executive ='fzf'
let g:indentLine_fileTypeExclude = ['dashboard']
let g:dashboard_custom_header = [
    \'',
    \'   ⣴⣶⣤⡤⠦⣤⣀⣤⠆     ⣈⣭⣭⣿⣶⣿⣦⣼⣆         ',
    \'    ⠉⠻⢿⣿⠿⣿⣿⣶⣦⠤⠄⡠⢾⣿⣿⡿⠋⠉⠉⠻⣿⣿⡛⣦       ',
    \'          ⠈⢿⣿⣟⠦ ⣾⣿⣿⣷⠄⠄⠄⠄⠻⠿⢿⣿⣧⣄     ',
    \'           ⣸⣿⣿⢧ ⢻⠻⣿⣿⣷⣄⣀⠄⠢⣀⡀⠈⠙⠿⠄    ',
    \'          ⢠⣿⣿⣿⠈  ⠡⠌⣻⣿⣿⣿⣿⣿⣿⣿⣛⣳⣤⣀⣀   ',
    \'   ⢠⣧⣶⣥⡤⢄ ⣸⣿⣿⠘⠄ ⢀⣴⣿⣿⡿⠛⣿⣿⣧⠈⢿⠿⠟⠛⠻⠿⠄  ',
    \'  ⣰⣿⣿⠛⠻⣿⣿⡦⢹⣿⣷   ⢊⣿⣿⡏  ⢸⣿⣿⡇ ⢀⣠⣄⣾⠄   ',
    \' ⣠⣿⠿⠛⠄⢀⣿⣿⣷⠘⢿⣿⣦⡀ ⢸⢿⣿⣿⣄ ⣸⣿⣿⡇⣪⣿⡿⠿⣿⣷⡄  ',
    \' ⠙⠃   ⣼⣿⡟  ⠈⠻⣿⣿⣦⣌⡇⠻⣿⣿⣷⣿⣿⣿ ⣿⣿⡇⠄⠛⠻⢷⣄ ',
    \'      ⢻⣿⣿⣄   ⠈⠻⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟ ⠫⢿⣿⡆     ',
    \'       ⠻⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣀⣤⣾⡿⠃     ',
    \'',]
lua <<EOF
vim.g.dashboard_custom_section = {
    a = {description = {' New file'}, command = 'DashboardNewFile'},
    b = {description = {' Browse files'}, command = 'Files'},
    c = {description = {' Settings'}, command = 'edit $HOME/.config/nvim/init.vim'},
    d = {description = {' Exit'}, command = 'exit'},
}
EOF

"	VimWiki:
let g:vimwiki_list = [
	\{'path': '~/.wiki/',
	\'syntax': 'markdown',
	\'ext': '.md',
	\'index': 'README',
	\},]
let g:vimwiki_markdown_link_ext = 1

"	FZF:
map <C-p> :Files<CR>
map <C-n> :Buffers<CR>
let g:fzf_buffers_jump = 1
let g:fzf_colors =
\ { 'fg':      ['fg', 'Normal'],
  \ 'bg':      ['bg', 'Normal'],
  \ 'hl':      ['fg', 'Comment'],
  \ 'fg+':     ['fg', 'CursorLine', 'CursorColumn', 'Normal'],
  \ 'bg+':     ['bg', 'CursorLine', 'CursorColumn'],
  \ 'hl+':     ['fg', 'Statement'],
  \ 'info':    ['fg', 'PreProc'],
  \ 'border':  ['fg', 'Ignore'],
  \ 'prompt':  ['fg', 'Conditional'],
  \ 'pointer': ['fg', 'Exception'],
  \ 'marker':  ['fg', 'Keyword'],
  \ 'spinner': ['fg', 'Label'],
  \ 'header':  ['fg', 'Comment'] }

"	Mappings:
let mapleader=' '
nnoremap Y y$
nnoremap J mzJ`z
nmap <leader>gs :G<CR>
nmap <F2> <Plug>(coc-rename)

"	Quick Run:
" autocmd filetype cpp nnoremap <buffer> <C-c> :!/opt/homebrew/Cellar/gcc/11.2.0/bin/aarch64-apple-darwin20-g++-11 -std=c++14 -Wshadow -Wall -o %:t:r % && ./%:t:r && echo '' && less ./o.txt<CR>
autocmd filetype cpp nnoremap <buffer> <C-c> :!g++ -std=c++14 -Wshadow -Wall -o %:t:r % -g -fsanitize=address -fsanitize=undefined -D_GLIBCXX_DEBUG && ./%:t:r && echo '' && less ./o.txt<CR>
autocmd filetype python nnoremap <buffer> <C-c> :!python3 %<CR>