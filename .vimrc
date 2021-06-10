call plug#begin('~/.vim/plugged')
	" Better Syntax Support
	Plug 'sheerun/vim-polyglot'
	" File Explorer
	Plug 'scrooloose/NERDTree'
	Plug 'ryanoasis/vim-devicons'
	" Auto pairs for '(' '[' '{'
	Plug 'jiangmiao/auto-pairs'
	" Rich Presence
	" Plug 'vimsence/vimsence'
	" AirLine 
	Plug 'vim-airline/vim-airline'
	Plug 'vim-airline/vim-airline-themes'
    source $HOME/.vim/themes/airline.vim
	" CSS color
	Plug 'ap/vim-css-color'
	" Surround
	Plug 'tpope/vim-surround'
	" Commentary	
	Plug 'tomtom/tcomment_vim'
	" Syntax Check (ale)
	Plug 'dense-analysis/ale'
	" CoC
	" Plug 'neoclide/coc.nvim', {'branch': 'release'}
	" source $HOME/.vim/plug-config/coc.vim
	" fzf
	Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    call plug#end()
    
:map<C-n>    :NERDTree<CR>
set clipboard=unnamedplus
set number
set tabstop=4
set shiftwidth=4
set expandtab
set cmdheight=1
set background=dark
set ignorecase
set smartcase

"Compile and Run
set autowrite
autocmd filetype cpp nnoremap <buffer> <C-c> :!g++ -std=c++17 -Wshadow -Wall -o %:t:r % -g -fsanitize=address -fsanitize=undefined -D_GLIBCXX_DEBUG && ./%:t:r<CR>
autocmd filetype python nnoremap <buffer> <C-c> :!python3 %<CR>
