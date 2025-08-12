return {

  -- File explorer
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    lazy = false,
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-tree/nvim-web-devicons",
      "MunifTanjim/nui.nvim",
    },
  },

  -- Status line
  { "nvim-lualine/lualine.nvim", lazy = false },

  -- Syntax highlighting
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate", lazy = false },

  -- Fuzzy finder
  {
    "nvim-telescope/telescope.nvim",
    lazy = false,
    dependencies = {
      "nvim-lua/plenary.nvim", -- Required for Telescope
    },
  },

  -- LSP support
  { "neovim/nvim-lspconfig", lazy = false },
  { "williamboman/mason.nvim", lazy = false },
  { "williamboman/mason-lspconfig.nvim", lazy = false },

  -- Autocompletion
  { "hrsh7th/nvim-cmp", lazy = false },
  { "hrsh7th/cmp-nvim-lsp", lazy = false },
  { "L3MON4D3/LuaSnip", lazy = false },

  -- Git integration
  { "lewis6991/gitsigns.nvim", lazy = false },

  -- Terminal integration
  {
    "akinsho/toggleterm.nvim",
    lazy = false,
    config = function()
      require("toggleterm").setup()
    end,
  },

  -- Theme
  { "tiagovla/tokyodark.nvim", lazy = false },

  -- Pywal theme integration
  {
    "AlphaTechnolog/pywal.nvim",
    lazy = false,
    config = function()
      require("pywal").setup()
      vim.cmd("colorscheme pywal")
    end,
  },
}

