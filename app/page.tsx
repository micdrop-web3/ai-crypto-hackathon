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
          <div className="collapse-title pl-0 font-medium">
            あなたの所有ポイント:
            <span className="ml-1 text-primary">999 PT</span>
          </div>
          <div className="collapse-content">
            <p>内容</p>
          </div>
        </div>
        <div className="collapse-arrow collapse lg:w-1/2">
          <input type="checkbox" className="peer" />
          <div className="collapse-title pl-0 font-medium">
            所有ポイントランキング
          </div>
          <div className="collapse-content">
            <p>内容</p>
          </div>
        </div>
      </article>
    </>
  );
}
