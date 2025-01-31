
type TikTokSearchResult = {
  type: number;
  item: {
    id: string;
    desc: string;
    createTime: number;
    video: {
      id: string;
      height: number;
      width: number;
      duration: number;
      ratio: string;
      cover: string;
      originCover: string;
      dynamicCover: string;
      playAddr: string;
      downloadAddr: string;
      shareCover: string[];
      reflowCover: string;
      bitRate: number;
      encodedType: 'normal';
      format: 'mp4';
      videoQuality: 'normal';
      encodeUserTag: string;
    }
    author: {
      id: string;
      uniqueId: string;
      nickname: string;
      avatarThumb: string;
      avatarMedium: string;
      avatarLarger: string;
      signature: string;
      verified: boolean;
      secUid: string;
      secret: boolean;
      ftc: boolean;
      relation: number;
      openFavorite: boolean;
      commentSetting: number;
      duetSetting: number;
      stitchSetting: number;
      privateAccount: boolean;
      donwnloadSetting: number;
    }
    music: {
      id: string;
      title: string | 'original sound';
      playUrl: string;
      coverThumb: string;
      coverMedium: string;
      coverLarge: string;
      authorName: string;
      original: boolean;
      duration: number;
      album: string;
    }
    challenges: {
      id: string;
      title: string;
      desc: string;
      profileThumb: string;
      profileMedium: string;
      profileLarger: string;
      coverThumb: string;
      coverMedium: string;
      coverLarger: string;
      isCommerce: boolean;
    }[]
    stats: {
      diggCount: number;
      shareCount: number;
      commentCount: number;
      playCount: number;
      collectCount: number;
    }
    duetInfo: {
      duetFromId: string;
    }
    originalItem: boolean;
    officialItem: boolean;
    textExtra: {
      awemeId: string;
      start: number;
      end: number;
      hashtagName: string;
      hashtagId: string;
      type: number;
      userId: string;
      isCommerce: boolean;
      userUniqueId: string;
      secUid: string;
      subType: number;
    }[]
    secret: boolean;
    forFriend: boolean;
    digged: boolean;
    itemCommentStatus: number;
    showNotPass: boolean;
    vl1: boolean;
    itemMute: boolean;
    authorStats: {
      followingCount: number;
      followerCount: number;
      heart: number;
      heartCount: number;
      videoCount: number;
      diggCount: number;
    }
    privateItem: boolean;
    duetEnabled: boolean;
    stitchEnabled: boolean;
    shareEnabled: boolean;
    isAd: boolean;
    collected: boolean;
  }
  common: {
    doc_id_str: string;
  }
}

declare module 'tiktok-search-api' {
  export function TikTokSearch(query: string, ttwid: string, limit: number): Promise<TikTokSearchResult[]>;
}