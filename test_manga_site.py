from mangasites.asura_gg import Asura

asura = Asura()

url = "https://www.asurascans.com/villain-to-kill-chapter-87/"

req = asura.Request(url)

images = asura.chapter_images(req)
print(images)