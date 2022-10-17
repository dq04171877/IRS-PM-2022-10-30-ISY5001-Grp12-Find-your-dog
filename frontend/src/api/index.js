import axios from 'axios'
const API_URL = 'http://127.0.0.1:5000/api'

export function fetchTitle(surveyId) {
    return axios.get(`${API_URL}/recommendation/query/${surveyId}/`)
}

const actions = {
    // asynchronous operations
    loadTitle(context, { title }) {
      return fetchTitle(title)
        .then((response) => {
          // context.commit('setSurvey', { survey: response })
          context.commit('setSurvey', { survey: response.data })
        })
    }
}