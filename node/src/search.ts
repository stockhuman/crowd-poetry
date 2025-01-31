const API_URL = "https://www.tiktok.com/api/search/general/full/?"

async function fetchTikTokSearch(
  keyword: string,
  ttwid: string,
  offset: number = 0,
  searchId?: string,
): Promise<TikTokSearchResult[]> {
  return new Promise(async (resolve) => {
    let urlString = API_URL
    let ops = [
      { name: "from_page", val: "search" },
      { name: "keyword", val: keyword },
      { name: "offset", val: offset },
    ]

    for (let b = 0; b < ops.length; b++) {
      urlString += ops[b].name + "=" + ops[b].val + "&"
    }

    if (searchId) {
      urlString += "search_id=" + searchId + "&"
    }

    try {
      fetch(urlString, {
        method: "GET",
        headers: {
          Cookie: "ttwid=" + ttwid + ";",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          resolve(data.data)
        })
    } catch (err) {
      console.log(err)
    }
  })
}

export async function TikTokSearch(
  keyword: string,
  ttwid: string,
  pages: number,
): Promise<TikTokSearchResult[]> {

  try {
    if (!keyword) return []
    const initialSearch = await fetchTikTokSearch(keyword, ttwid)
    if (!initialSearch) {
      return []
    }
    const searchId = initialSearch[0].common.doc_id_str
    let results: TikTokSearchResult[] = []
    for (let i = 1; i < pages; i++) {
      const offset = i * 12
      const search = await fetchTikTokSearch(keyword, ttwid, offset, searchId)
      results = results.concat(search)
    }
    return results
  } catch (e) {
    console.error(e)
    return []
  }
}
