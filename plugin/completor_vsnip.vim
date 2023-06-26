if exists('g:loaded_completor_vsnip_plugin')
    finish
endif

let g:loaded_completor_vsnip_plugin = 1
let s:py = has('python3') ? 'py3' : 'py'


function! s:err(msg) abort
    echohl Error
    echo a:msg
    echohl NONE
endfunction


function! s:import_python() abort
    try
        exe s:py 'import completor_vsnip'
    catch /^Vim(py\(thon\|3\)):/
        call s:err('Fail to import completor_vsnip')
        return
    endtry

    try
        exe s:py 'import completor, completers.common'
    catch /^Vim(py\(thon\|3\)):/
        call s:err('Fail to import completor')
        return
    endtry

    try
        exe s:py 'completor.get("common").hooks.append(completor_vsnip.Vsnip.filetype)'
    catch /^Vim(py\(thon\|3\)):/
        call s:err('Fail to add vsnip hook')
    endtry
endfunction


function! s:enable() abort
    call s:import_python()
    call s:disable()
endfunction


function! s:disable() abort
    augroup completor_vsnip
        autocmd!
    augroup END
endfunction


augroup completor_vsnip
    autocmd!
    autocmd InsertEnter * call s:enable()
augroup END
