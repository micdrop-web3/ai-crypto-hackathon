import Breadcrumb from '@/app/_components/Breadcrumb';
import {
  CheckIcon,
  XMarkIcon as XMarkIconMini,
} from '@heroicons/react/20/solid';
import Image from 'next/image';
import { ComponentProps } from 'react';

const badges = [
  {
    name: 'バッジ1',
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80',
  },
  // More people...
] as const;

const rankingUsers = [
  {
    rank: 1,
    name: 'Leslie Alexander',
    point: 11111111,
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    lastSeen: '3h ago',
    lastSeenDateTime: '2023-01-23T13:23Z',
  },
  {
    rank: 2,
    name: 'Dries Vincent',
    point: 22222222,
    imageUrl:
      'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    lastSeen: '3h ago',
    lastSeenDateTime: '2023-01-23T13:23Z',
  },
  {
    rank: 3,
    name: 'Dries Vincent',
    point: 33333333,
    imageUrl:
      'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
  },
] as const;

const pricing = {
  tier: {
    name: '',
    point: 10000,
    id: 'tier-scale',
    href: '#',
    featured: true,
  },
  section: {
    name: '',
    features: [
      {
        name: 'Tax Savings',
        tiers: true,
      },
      {
        name: 'Easy to use accounting',
        tiers: true,
      },
      {
        name: 'Multi-accounts',
        tiers: true,
      },
      {
        name: 'Invoicing',
        tiers: true,
      },
      {
        name: 'Exclusive offers',
        tiers: true,
      },
      {
        name: '6 months free advisor',
        tiers: true,
      },
      {
        name: 'Mobile and web access',
        tiers: true,
      },
    ],
  },
} as const;

export default function Page({ params }: { params: { id: number } }) {
  const breadcrumbProps: ComponentProps<typeof Breadcrumb> = {
    routes: [
      {
        href: '/ai-tubers',
        name: 'AITuber',
      },
      {
        href: `/ai-tubers/${params.id}`,
        name: 'AITuber詳細',
      },
    ],
    title: 'AITuber詳細',
  };

  return (
    <>
      <Breadcrumb {...breadcrumbProps}></Breadcrumb>
      <article>
        <div className="mt-5">
          {/* TODO おそらく詳細のアイコンに変わる */}
          <div className="flex items-center gap-x-6">
            <Image
              className="inline-block h-32 w-32 rounded-full"
              src="/sample/icon1.png"
              alt=""
              width={128}
              height={128}
            />
            <div>
              <h2 className="text-base font-semibold leading-7 tracking-tight text-gray-900">
                ここにAITuberの名前？
              </h2>
            </div>
          </div>
        </div>
        <div className="mt-10 border-b border-gray-200 pb-3">
          <h2 className="text-xl font-semibold leading-6 text-gray-900">
            あなたの所有ポイント
          </h2>
        </div>
        <div className="max-w-7xl">
          <ul
            role="list"
            className="mx-auto mt-5 grid max-w-2xl grid-cols-1 gap-x-6 gap-y-20 sm:grid-cols-2 lg:max-w-4xl lg:gap-x-8 xl:max-w-none"
          >
            {badges.map((badge) => (
              <li key={badge.name} className="flex flex-col gap-6 xl:flex-row">
                <img
                  className="aspect-[1/1] w-24 flex-none rounded-2xl object-cover"
                  src={badge.imageUrl}
                  alt=""
                />
              </li>
            ))}
          </ul>
        </div>
        <div className="mt-10 border-b border-gray-200 pb-3">
          <h2 className="text-xl font-semibold leading-6 text-gray-900">
            所有ポイントランキング
          </h2>
        </div>
        <ul role="list" className="divide-y divide-gray-100">
          {rankingUsers.map((rankingUser) => (
            <li
              key={rankingUser.rank}
              className="flex justify-between gap-x-6 py-5"
            >
              <div className="flex gap-x-4">
                <div className="flex items-center">{rankingUser.rank}</div>
                <img
                  className="h-12 w-12 flex-none rounded-full bg-gray-50"
                  src={rankingUser.imageUrl}
                  alt=""
                />
                <div className="min-w-0 flex-auto">
                  <p className="text-sm font-semibold leading-6 text-gray-900">
                    {rankingUser.name}
                  </p>
                  <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                    {rankingUser.point} ポイント
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ul>
        <h2 className="mt-10 text-xl font-semibold leading-6 text-gray-900">
          特典
        </h2>
        <section className="mt-2">
          <dl className="divide-y divide-gray-200 text-sm leading-6">
            {pricing.section.features.map((feature) => (
              <div
                key={feature.name}
                className="flex items-center justify-between py-3 sm:grid sm:grid-cols-2 sm:px-0"
              >
                <dt className="pr-4 text-gray-600">{feature.name}</dt>
                <dd className="flex items-center justify-end sm:justify-center sm:px-4">
                  {feature.tiers ? (
                    <CheckIcon
                      className="mx-auto h-5 w-5 text-indigo-600"
                      aria-hidden="true"
                    />
                  ) : (
                    <XMarkIconMini
                      className="mx-auto h-5 w-5 text-gray-400"
                      aria-hidden="true"
                    />
                  )}
                </dd>
              </div>
            ))}
          </dl>
        </section>
      </article>
    </>
  );
}
