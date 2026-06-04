import api from './index'

export const getMyActivity = () => api.get('/analytics/my-activity/')
export const getMySummary = () => api.get('/analytics/my-summary/')
export const getPopularPapers = () => api.get('/analytics/popular-papers/')
export const getTrendingTopics = () => api.get('/analytics/trending-topics/')
export const getSystemOverview = () => api.get('/analytics/system-overview/')
export const getUserStats = () => api.get('/analytics/user-stats/')
