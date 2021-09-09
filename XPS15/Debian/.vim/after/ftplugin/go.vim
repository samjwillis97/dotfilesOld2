compiler go
nnoremap <buffer> <space> :silent make <bar> redraw!<CR>
nnoremap <buffer> <F7> :terminal go run %<CR>
set termwinsize=10x0

set shiftwidth=2
set tabstop=2
set softtabstop=2
set noexpandtab
set autoindent
set smartindent

" User-defined command for running gofmt on select lines (default all)
:command! -buffer -range=% Gofmt let b:winview = winsaveview() |
  \ silent! execute <line1> . "," . <line2> . "!gofmt " | 
  \ call winrestview(b:winview)

" User-defined command for running goimport on select lines (default all)
:command! -buffer -range=% Goimport let b:winview = winsaveview() |
  \ silent! execute <line1> . "," . <line2> . "!goimports " | 
  \ call winrestview(b:winview)

" Autocommand for running gofmt and goimport on buffer saves
