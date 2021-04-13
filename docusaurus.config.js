module.exports = {
  title: 'StructNoSQL',
  tagline: 'Structured document based NoSQL client for AWS DynamoDB with automatic data validation ' +
      'and advanced database queries functions. Compatible with Serverless applications.',
  url: 'https://engine.inoft.com/StructNoSQL',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'inoft', // Usually your GitHub org/user name.
  projectName: 'StructNoSQL', // Usually your repo name.
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
    localeConfigs: {
      fr: {
        label: 'Français',
      },
      en: {
        label: 'English',
      },
    },
  },
  themeConfig: {
    navbar: {
      title: 'StructNoSQL',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          to: 'docs/',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {to: 'blog', label: 'Blog', position: 'left'},
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/Robinson04/StructNoSQL',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Style Guide',
              to: 'docs/',
            },
            {
              label: 'Second Doc',
              to: 'docs/doc2/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/4dQPHTu',
            }
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: 'blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/Robinson04/StructNoSQL',
            },
          ],
        },
      ],
      copyright: `Inoft 2020 - ${new Date().getFullYear()}. Construis avec Docusaurus.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl: 'https://github.com/Robinson04/StructNoSQL_docs/edit/master/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/facebook/docusaurus/edit/master/website/blog/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
