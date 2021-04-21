import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import CodeBlock from '@docusaurus/theme-classic/lib-next/theme/CodeBlock';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './src/pages/styles.module.css';


/*
      <>
        Docusaurus was designed from the ground up to be easily installed and
        used to get your website up and running quickly.
      </>
 */

/*
class UsersTableModel(TableDataModel):


    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class FriendModel(MapModel):
        relationshipStatus = BaseField(name='relationshipStatus', field_type=str, required=False)
    friends = BaseField(name='friends', field_type=Dict[str, FriendModel], index_name='friendId', required=False)
 */

const features = [
  {
    title: 'Centralized smart data validation',
    description: (<>
        If some items in a dictionary or list, or some non-required attributes in an item are not matching your data model, by default,
        instead of blindly crashing, all the non-required invalid data will be removed, and the valid data will be send to your database.
    </>),
  },
  {
    title: 'Expressive models and infrastructure',
    imageUrl: 'img/undraw_docusaurus_tree.svg',
    description: (
      <>
        Support for Dictionary, List, Sets, Maps, Nested objects, Secondary Indexes to sort data by different fields,
        automatic separation of operations into multiples requests when reaching the maximum size per operation, and more.
      </>
    ),
  },
  {
    title: 'Compatible with Serverless applications',
    imageUrl: 'img/lambda_logo.png',
    description: (
      <>
        The library not require any external services, does not impose any scaling limitation,
        and will by default configure your databases tables to be fully serverless.
      </>
    ),
  },
  {
    title: 'Open-source under the MIT License',
    imageUrl: 'img/lambda_logo.png',
    description: (
      <>
        Do what you want.
      </>
    ),
  },
];

function Feature({imageUrl, title, description}) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default function Home() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={clsx('button button--outline button--secondary button--lg', styles.getStarted)}
              to={useBaseUrl('docs/')}>
              Get Started
            </Link>
          </div>
        </div>
      </header>
    </Layout>
  );
}

/*
      <main>
        {features && features.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                  <h2>Step 1 - Create a table model</h2>
                  <CodeBlock className="python" children={
"from StructNoSQL import TableDataModel, BaseField, MapModel\n" +
"from typing import Dict\n" +
"\n" +
"class UsersTableModel(TableDataModel):\n" +
"    userId = BaseField(name='userId', field_type=str, required=True)\n" +
"    username = BaseField(name='username', field_type=str, required=False)\n" +
"    class FriendModel(MapModel):\n" +
"        relationshipStatus = BaseField(name='relationshipStatus', field_type=str, required=False)\n" +
"    friends = BaseField(name='friends', field_type=Dict[str, FriendModel], index_name='friendId', required=False)\n"
                  }>
        </CodeBlock>
                {features.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
 */
