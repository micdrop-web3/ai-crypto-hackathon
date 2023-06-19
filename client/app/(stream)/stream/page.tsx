'use client';

import { DisplayValue } from '@/app/_consts/displays';
import { useSearchParams } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';

type Rank = {
  id: number;
  rank: number;
  icon: string;
  name: string;
  comment: string;
};

type Comment = {
  id: number;
  icon: string;
  name: string;
  comment: string;
};

const shuffleArray = (array: string[]) => {
  const cloneArray = [...array];

  for (let i = cloneArray.length - 1; i >= 0; i--) {
    const rand = Math.floor(Math.random() * (i + 1));
    // 配列の要素の順番を入れ替える
    const tmpStorage = cloneArray[i];
    cloneArray[i] = cloneArray[rand];
    cloneArray[rand] = tmpStorage;
  }

  return cloneArray;
};

export default function Page() {
  const searchParams = useSearchParams();
  const liveId = searchParams.get('liveId');
  const displays = searchParams.getAll('displays') as DisplayValue[];

  const commentsRef = useRef<HTMLUListElement>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [pointRanks, setPointRanks] = useState<Rank[]>([]);
  const [superChatRanks, setSuperChatRanks] = useState<Rank[]>([]);
  const [commentRanks, setCommentRanks] = useState<Rank[]>([]);

  useEffect(() => {
    const callback = async () => {
      // TODO APIから取得するように変更する
      // const response = await fetch('http://localhost:3000/');
      // const data = await response.json();

      const dummyNames = ['名前1', '名前2', '名前3', '名前4', '名前5'];
      const dummyNums = [10000, 1000, 100, 10, 1];
      setCommentRanks(() => {
        if (!displays.includes('commentRank')) {
          return [];
        }

        return shuffleArray(dummyNames).map((name, index) => {
          return {
            id: index + 1,
            rank: index + 1,
            icon: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            name,
            comment: `${dummyNums[index]}`,
          };
        });
      });
      setPointRanks(() => {
        if (!displays.includes('pointRank')) {
          return [];
        }

        return shuffleArray(dummyNames).map((name, index) => {
          return {
            id: index + 1,
            rank: index + 1,
            icon: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            name,
            comment: `${dummyNums[index]}`,
          };
        });
      });
      setSuperChatRanks(() => {
        if (!displays.includes('superChatRank')) {
          return [];
        }

        return shuffleArray(dummyNames).map((name, index) => {
          return {
            id: index + 1,
            rank: index + 1,
            icon: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            name,
            comment: `${dummyNums[index]}`,
          };
        });
      });
      setComments((oldValue) => {
        if (!displays.includes('comment')) {
          return [];
        }

        return [
          ...oldValue,
          {
            id: oldValue.length + 1,
            icon: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
            name: '名前',
            comment: `コメント${oldValue.length + 1}`,
          },
        ];
      });

      if (!commentsRef || !commentsRef.current) {
        return;
      }
      // 一番下までスクロール
      commentsRef.current.scrollTop = commentsRef.current.scrollHeight;
    };

    callback();
    const interval = setInterval(callback, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-2 gap-5	p-10">
      {comments.length > 0 && (
        <div className="rounded-xl border border-black bg-white p-5">
          <h2 className="text-4xl font-semibold leading-6 text-black">
            コメント
          </h2>
          <ul
            role="list"
            className="mt-5 max-h-96 overflow-y-scroll"
            id="comments"
            ref={commentsRef}
          >
            {comments.map((comment) => (
              <li
                key={comment.id}
                className="flex content-center items-center gap-x-2 py-4"
              >
                <img
                  className="inline-block h-9 w-9 rounded-full"
                  src={comment.icon}
                  alt=""
                  width={128}
                  height={128}
                />
                <span className="font-semibold">{comment.name}</span>
                <span>{comment.comment}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {pointRanks.length > 0 && (
        <div className="rounded-xl border border-black bg-white p-5">
          <h2 className="text-4xl font-semibold leading-6 text-black">
            獲得ポイント
          </h2>
          <ul role="list" className="mt-5 max-h-96">
            {pointRanks.map((pointRank) => (
              <li
                key={pointRank.id}
                className="flex content-center items-center gap-x-2 py-4"
              >
                <span className="font-semibold">{pointRank.rank} 位</span>
                <img
                  className="inline-block h-9 w-9 rounded-full"
                  src={pointRank.icon}
                  alt=""
                  width={128}
                  height={128}
                />
                <span className="font-semibold">{pointRank.name}</span>
                <span>{pointRank.comment}ポイント</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {superChatRanks.length > 0 && (
        <div className="rounded-xl border border-black bg-white p-5">
          <h2 className="text-4xl font-semibold leading-6 text-black">
            スーパーチャット
          </h2>
          <ul role="list" className="mt-5 max-h-96">
            {superChatRanks.map((superChatRank) => (
              <li
                key={superChatRank.id}
                className="flex content-center items-center gap-x-2 py-4"
              >
                <span className="font-semibold">{superChatRank.rank} 位</span>
                <img
                  className="inline-block h-9 w-9 rounded-full"
                  src={superChatRank.icon}
                  alt=""
                  width={128}
                  height={128}
                />
                <span className="font-semibold">{superChatRank.name}</span>
                <span>{superChatRank.comment}円</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {commentRanks.length > 0 && (
        <div className="rounded-xl border border-black bg-white p-5">
          <h2 className="text-4xl font-semibold leading-6 text-black">
            コメント回数
          </h2>
          <ul role="list" className="mt-5 max-h-96">
            {commentRanks.map((commentRank) => (
              <li
                key={commentRank.id}
                className="flex content-center items-center gap-x-2 py-4"
              >
                <span className="font-semibold">{commentRank.rank}位</span>
                <img
                  className="inline-block h-9 w-9 rounded-full"
                  src={commentRank.icon}
                  alt=""
                  width={128}
                  height={128}
                />
                <span className="font-semibold">{commentRank.name}</span>
                <span>{commentRank.comment}回</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
