'use client';

import { ArrowTopRightOnSquareIcon } from '@heroicons/react/20/solid';
import { useRef } from 'react';

export default function Page() {
  const liveIdRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const liveId = liveIdRef.current?.value;
    if (!liveId) {
      return;
    }

    const params = new URLSearchParams();
    params.set('liveId', liveId);
    // 新しいウインドウで開くため、router.push()は使わない
    window.open(`/stream?${params.toString()}`, '_ blank');
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="max-w-5xl">
        <label
          htmlFor="liveId"
          className="block text-lg font-semibold leading-6 text-gray-900"
        >
          YouTube LiveのLive ID
        </label>
        <div className="mt-2">
          <input
            type="text"
            name="liveId"
            id="liveId"
            ref={liveIdRef}
            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            placeholder="you@example.com"
          />
        </div>
        <div className="mt-5">
          <button
            type="submit"
            className="flex w-full justify-center gap-x-2 rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            <ArrowTopRightOnSquareIcon className="h-6 w-6 shrink-0"></ArrowTopRightOnSquareIcon>
            背景画像を新規タブで開く
          </button>
        </div>
      </form>
    </>
  );
}
