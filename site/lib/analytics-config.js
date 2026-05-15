export const analyticsConfig = {
  baidu: {
    enabled: process.env.NODE_ENV === 'production',
    siteId: '8864588cde35a2181784b07b34f770f9',
  },
  google: {
    enabled: process.env.NODE_ENV === 'production',
    measurementId: 'G-C3YEYVPEBR',
  },
}
