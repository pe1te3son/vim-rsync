" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------


function! InitiateFileSync()
if exists("g:SERVER_HOST")
python << endOfPython
from vimrsync import vimrsync

# DO IT WITH TIMESTAMP
current_c = vim.eval("g:airline_section_c")
#vim.command("let g:airline_section_c = 'syncing "+ current_c  +"' | AirlineRefresh")


current_working_file = vim.eval("expand('%:p')")
vimrsync.initiate_file_sync(current_working_file, {
  "SERVER_HOST": vim.eval("g:SERVER_HOST"),
  "APPS": vim.eval("g:APPS")
})
endOfPython
else
  echo "SERVER_HOST must be defined"
endif

endfunction



function! InitiateAppSync()

if exists("g:SERVER_HOST") && exists("g:APPS")
python << endOfPython
from vimrsync import vimrsync

current_working_file = vim.eval("expand('%:p')")
vimrsync.initiate_app_sync(current_working_file, {
  "SERVER_HOST": vim.eval("g:SERVER_HOST"),
  "APPS": vim.eval("g:APPS")
})
endOfPython
else
  echo "SERVER_HOST and APPS must be defined"
endif

endfunction
" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! VimRsyncFile call InitiateFileSync()
command! VimRsyncApp call InitiateAppSync()
