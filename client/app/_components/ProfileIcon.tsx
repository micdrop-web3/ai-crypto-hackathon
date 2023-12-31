const ProfileIcon = () => {
  return (
    <div className="flex items-center">
      <div>
        <img
          className="inline-block h-9 w-9 rounded-full"
          src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
          alt=""
          width={128}
          height={128}
        />
      </div>
      <div className="ml-3">
        <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900">
          自分のアカウント名
        </p>
        <p className="text-xs font-medium text-gray-500 group-hover:text-gray-700">
          0xfa16...9999
        </p>
      </div>
    </div>
  );
};
export default ProfileIcon;
