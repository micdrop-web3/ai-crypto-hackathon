'use client';

import { useSearchParams } from 'next/navigation';

export default function Page() {
  const searchParams = useSearchParams();
  const liveId = searchParams.get('liveId');
  console.log(liveId);
  return <>あああ</>;
}
