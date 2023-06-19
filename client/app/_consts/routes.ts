import {
  Cog8ToothIcon,
  GiftIcon,
  HomeIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
} from '@heroicons/react/24/outline';

export const routes = [
  { name: 'トップページ', href: '#', icon: HomeIcon, sidebar: true },
  {
    name: '検索',
    href: '#',
    icon: MagnifyingGlassIcon,
    sidebar: true,
  },
  { name: 'ポイント取引', href: '#', icon: GiftIcon, sidebar: true },
  {
    name: 'ヘルプ',
    href: '#',
    icon: QuestionMarkCircleIcon,
    sidebar: true,
  },
  { name: '設定', href: '#', icon: Cog8ToothIcon, sidebar: true },
] as const;
