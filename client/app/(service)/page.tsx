'use client';

import { displays, DisplayValue } from '@/app/_consts/displays';
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/20/solid';
import { SubmitHandler, useForm } from 'react-hook-form';

type SubmitData = {
  liveId: string;
  displays: DisplayValue | DisplayValue[];
};

export default function Page() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SubmitData>();

  const onSubmit: SubmitHandler<SubmitData> = (data: SubmitData) => {
    console.log(data);
    const params = new URLSearchParams();
    params.set('liveId', data.liveId);
    if (data.displays instanceof Array) {
      data.displays.forEach((display) => {
        params.append('displays', display);
      });
    } else {
      params.set('displays', data.displays);
    }
    // 新しいウインドウで開くため、router.push()は使わない
    window.open(`/stream?${params.toString()}`, '_ blank');
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-5xl">
        <label className="text-lg font-semibold leading-6 text-gray-900">
          YouTube LiveのLive ID
          {errors.liveId && (
            <div className="mt-2 text-sm font-normal text-red-700">
              {errors.liveId.message}
            </div>
          )}
          <div className="mt-2">
            <input
              type="text"
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              {...register('liveId', {
                required: 'YouTube LiveのLive IDを選択してください',
              })}
            />
          </div>
        </label>

        <h2 className="mt-10 text-lg font-semibold leading-6 text-gray-900">
          表示したい項目（最大3つ）
        </h2>
        {errors.displays && (
          <div className="mt-2 text-sm font-normal text-red-700">
            {errors.displays.message}
          </div>
        )}
        {displays.map((display) => (
          <label
            className="mt-5 flex items-center gap-x-2  text-gray-900"
            key={display.value}
          >
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
              value={display.value}
              {...register('displays', {
                validate: (value) =>
                  (value && value.length <= 3) || '最大3つまで選択してください',
              })}
            />
            <span className="">{display.text}</span>
          </label>
        ))}
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
