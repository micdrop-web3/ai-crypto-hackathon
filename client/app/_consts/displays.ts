export const displays = [
  {
    value: 'comment',
    text: 'コメント',
  },
  {
    value: 'pointRank',
    text: '獲得ポイントランキング',
  },
  {
    value: 'superChatRank',
    text: 'スーパーチャットランキング',
  },
  {
    value: 'commentRank',
    text: 'コメント回数ランキング',
  },
] as const;

export type DisplayValue = (typeof displays)[number]['value'];
