import api from './index'

export const getFavorites = () => api.get('/favorites/')
export const getFavoritePapers = () => api.get('/favorites/papers/')
export const getFavoriteProjects = () => api.get('/favorites/projects/')
export const addFavorite = (data) => api.post('/favorites/', data)
export const removeFavorite = (id) => api.delete(`/favorites/${id}/`)
export const checkFavorite = (data) => api.post('/favorites/check/', data)
