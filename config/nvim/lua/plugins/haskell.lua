return {
  {
    "neovimhaskell/haskell-vim",
    ft = { "haskell", "lhaskell", "cabal" }, -- Load for Haskell filetypes
    config = function()
      -- Optional: Customize haskell-vim settings
      vim.g.haskell_classic_highlighting = 1 -- Use traditional highlighting
      vim.g.haskell_indent_if = 2 -- Align 'then' two spaces after 'if'
      vim.g.haskell_indent_case = 2 -- Indent case expressions
      vim.g.haskell_indent_let = 4 -- Indent let blocks
      vim.g.haskell_indent_where = 2 -- Indent where clauses
      vim.g.haskell_indent_do = 3 -- Indent do blocks
      vim.g.haskell_indent_in = 0 -- Align 'in' with 'let'
      vim.g.haskell_indent_before_where = 2
      vim.g.haskell_indent_after_bare_where = 2
    end,
  },
}
