-- Set leader key
vim.g.mapleader = " "

local map = vim.keymap.set
local opts = { noremap = true, silent = true }

-- Neo-tree
vim.keymap.set("n", "<leader>e", ":Neotree toggle<CR>", { noremap = true, silent = true })

-- Telescope
map("n", "<leader>ff", ":Telescope find_files<CR>", opts)
map("n", "<leader>fg", ":Telescope live_grep<CR>", opts)
map("n", "<leader>fb", ":Telescope buffers<CR>", opts)

-- Toggleterm
map("n", "<leader>t", ":ToggleTerm<CR>", opts)

-- LSP
map("n", "gd", vim.lsp.buf.definition, opts)
map("n", "K", vim.lsp.buf.hover, opts)
map("n", "<leader>rn", vim.lsp.buf.rename, opts)
map("n", "<leader>ca", vim.lsp.buf.code_action, opts)

-- Gitsigns
map("n", "]c", ":Gitsigns next_hunk<CR>", opts)
map("n", "[c", ":Gitsigns prev_hunk<CR>", opts)
map("n", "<leader>hs", ":Gitsigns stage_hunk<CR>", opts)

