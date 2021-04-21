module.exports = {
  title: 'StructNoSQL',
  tagline: 'Structured document based NoSQL client for AWS DynamoDB with automatic data validation ' +
      'and advanced database queries functions. Compatible with Serverless applications.',
  url: 'https://engine.inoft.com/StructNoSQL',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'Inoft',
  projectName: 'StructNoSQL',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],  // , 'fr'],
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
        alt: 'Inoft Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          to: '/',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        // {to: 'blog', label: 'Blog', position: 'left'},
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
            {label: 'Basics', to: '/',},
            {label: 'API', to: '/api/put_record',},
            {label: 'Details', to: '/details/performances',},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'Discord', href: 'https://discord.gg/4dQPHTu'},
            {label: 'Github', href: 'https://github.com/Robinson04/StructNoSQL/issues'},
          ],
        },
        /*{
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
        },*/
      ],
      copyright: `Inoft 2020 - ${new Date().getFullYear()}. Built with Docusaurus.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/Robinson04/StructNoSQL_docs/edit/main/',
          routeBasePath: '/',
        },
        /*blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/Robinson04/StructNoSQL_docs/edit/main/',
        },*/
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
