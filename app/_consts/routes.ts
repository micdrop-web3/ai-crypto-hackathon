import {
  Cog8ToothIcon,
  GiftIcon,
  HomeIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
} from '@heroicons/react/24/outline';

export const routes = [
  { name: 'ダッシュボード', href: '/', icon: HomeIcon, sidebar: true },
  {
    name: 'AITuber',
    href: '/ai-tubers',
    icon: MagnifyingGlassIcon,
    sidebar: true,
  },
  { name: 'ポイント受取', href: '/gift', icon: GiftIcon, sidebar: true },
  {
    name: 'ヘルプ',
    href: '/help',
    icon: QuestionMarkCircleIcon,
    sidebar: true,
  },
  { name: '設定', href: '/setting', icon: Cog8ToothIcon, sidebar: true },
] as const;
