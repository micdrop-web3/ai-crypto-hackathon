'use client';

import { ChevronRightIcon } from '@heroicons/react/20/solid';
import Link from 'next/link';

const Breadcrumb: React.FC<{
  routes: { name: string; href: string }[]; // TODO 型を付けたい
  title: string;
}> = ({ routes, title }) => {
  return (
    <div>
      <nav className="flex" aria-label="Breadcrumb">
        <ol role="list" className="flex items-center space-x-4">
          {routes.map((route, index) => (
            <li key={index}>
              {index === 0 ? (
                <div className="flex">
                  <Link
                    href={route.href}
                    className="text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    {route.name}
                  </Link>
                </div>
              ) : (
                <div className="flex items-center">
                  <ChevronRightIcon
                    className="h-5 w-5 flex-shrink-0 text-gray-400"
                    aria-hidden="true"
                  />
                  <Link
                    href={route.href}
                    className="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
                  >
                    {route.name}
                  </Link>
                </div>
              )}
            </li>
          ))}
        </ol>
      </nav>
      <div className="mt-2 md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            {title}
          </h1>
        </div>
      </div>
    </div>
  );
};
export default Breadcrumb;
