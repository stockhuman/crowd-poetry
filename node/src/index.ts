import { TikTokSearch } from "./search"
import "dotenv/config"
import fs from "node:fs"

const ttwid = process.env.TTWID as string

console.log("Searching for", process.argv[2])

async function run() {
  try {
    const res = await TikTokSearch(process.argv[2], ttwid, 4)

    const videos = res
      .map(({ item }) => {
        if (!item) {
          return null
        }
        return {
          isAd: item.isAd,
          file: item.video.playAddr,
          title: item.desc,
          author: item.author.nickname,
          original: item.music.original,
        }
      })
      .filter((object) => object !== null)
      .filter((object) => object.original)

    fs.writeFile("./data.json", JSON.stringify(videos), (err) => {
      if (err) throw err
      console.log("Data has been written to file")
    })
  } catch (e) {
    console.error(e)
  }
}

run()
