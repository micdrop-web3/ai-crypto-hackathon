import ProfileIcon from '@/app/_components/ProfileIcon';

export default function Page() {
  return (
    <>
      <h1 className="text-2xl font-bold">ダッシュボード</h1>
      <article>
        <div className="mt-5">
          <ProfileIcon></ProfileIcon>
        </div>
        <div className="collapse-arrow collapse mt-5 lg:w-1/2">
          <input type="checkbox" className="peer" />
          <h2 className="collapse-title pl-0 font-semibold">
            あなたの所有ポイント:
            <span className="ml-1 text-primary-focus">999 PT</span>
          </h2>
          <div className="collapse-content">
            <p>内容</p>
          </div>
        </div>
        <div className="collapse-arrow collapse lg:w-1/2">
          <input type="checkbox" className="peer" />
          <h2 className="collapse-title pl-0 font-semibold">
            所有ポイントランキング
          </h2>
          <div className="collapse-content">
            <p>内容</p>
          </div>
        </div>
        <h2 className="mt-10 font-semibold">特典</h2>
      </article>
    </>
  );
}
