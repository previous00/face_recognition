import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_community.settings')
django.setup()

from movies.models import Category, Movie
from users.models import User
from reviews.models import Review, Comment
from favorites.models import Favorite
from datetime import date

admin = User.objects.get(username='admin')

categories_data = ['动作', '喜剧', '科幻', '爱情', '悬疑', '动画', '剧情']
categories = {}
for name in categories_data:
    cat, _ = Category.objects.get_or_create(name=name)
    categories[name] = cat

movies_data = [
    {'title': '肖申克的救赎', 'description': '一部关于希望与自由的经典之作。银行家安迪因被冤枉杀妻及其情人而被判无期徒刑，在肖申克监狱中，他用智慧和毅力改变了自己和周围人的命运。', 'director': '弗兰克·德拉邦特', 'actors': '蒂姆·罗宾斯, 摩根·弗里曼', 'release_date': date(1994, 9, 23), 'duration': 142, 'category': categories['剧情'], 'rating': 9.7},
    {'title': '星际穿越', 'description': '在未来的地球上，农作物因枯萎病而逐渐无法生长。前NASA宇航员库珀被选中穿越虫洞，寻找适合人类移民的新星球。', 'director': '克里斯托弗·诺兰', 'actors': '马修·麦康纳, 安妮·海瑟薇', 'release_date': date(2014, 11, 7), 'duration': 169, 'category': categories['科幻'], 'rating': 9.4},
    {'title': '千与千寻', 'description': '少女千寻随父母搬家途中误入了一个神灵休憩的世界，在这里她必须学会坚强和独立，才能拯救变成猪的父母。', 'director': '宫崎骏', 'actors': '柊瑠美, 入野自由', 'release_date': date(2001, 7, 20), 'duration': 125, 'category': categories['动画'], 'rating': 9.4},
    {'title': '盗梦空间', 'description': '道姆·柯布是一位经验丰富的窃贼，他在人们精神最脆弱的时候——梦境中，窃取潜意识中有价值的秘密。', 'director': '克里斯托弗·诺兰', 'actors': '莱昂纳多·迪卡普里奥, 渡边谦', 'release_date': date(2010, 7, 16), 'duration': 148, 'category': categories['科幻'], 'rating': 9.3},
    {'title': '泰坦尼克号', 'description': '1912年，泰坦尼克号从英国出发驶往美国纽约。贵族女孩罗丝与画家杰克在船上相遇相爱，然而船撞上了冰山。', 'director': '詹姆斯·卡梅隆', 'actors': '莱昂纳多·迪卡普里奥, 凯特·温丝莱特', 'release_date': date(1997, 12, 19), 'duration': 194, 'category': categories['爱情'], 'rating': 9.4},
    {'title': '疯狂动物城', 'description': '一个所有动物和平共处的世界里，兔子朱迪成为了第一位兔子警官。她与狐狸尼克搭档破获了一桩惊天阴谋。', 'director': '拜伦·霍华德', 'actors': '金妮弗·古德温, 杰森·贝特曼', 'release_date': date(2016, 3, 4), 'duration': 108, 'category': categories['动画'], 'rating': 9.2},
    {'title': '功夫', 'description': '阿星是一个落魄的小人物，他一心想加入斧头帮做坏事。但一系列阴差阳错后，他发现了自己惊人的武学天赋。', 'director': '周星驰', 'actors': '周星驰, 元华, 黄圣依', 'release_date': date(2004, 12, 23), 'duration': 95, 'category': categories['喜剧'], 'rating': 9.0},
    {'title': '速度与激情7', 'description': '多米尼克和他的团队以为一切回归平静，但一个神秘的杀手肖·欧文出现了，要为其弟弟报仇。', 'director': '温子仁', 'actors': '范·迪塞尔, 保罗·沃克', 'release_date': date(2015, 4, 3), 'duration': 137, 'category': categories['动作'], 'rating': 8.5},
]

for m in movies_data:
    Movie.objects.get_or_create(title=m['title'], defaults={**m, 'created_by': admin})

user1, _ = User.objects.get_or_create(username='filmfan', defaults={'nickname': '电影迷小王'})
if not user1.has_usable_password():
    user1.set_password('123456')
    user1.save()

user2, _ = User.objects.get_or_create(username='movielover', defaults={'nickname': '影评达人'})
if not user2.has_usable_password():
    user2.set_password('123456')
    user2.save()

movie1 = Movie.objects.get(title='肖申克的救赎')
movie2 = Movie.objects.get(title='星际穿越')

r1, _ = Review.objects.get_or_create(user=user1, movie=movie1, defaults={'title': '希望是件美好的事', 'content': '这是一部关于希望、自由和坚持的电影。安迪用了20年的时间证明了一件事：人只要有希望，就永远不会被真正的囚禁。这部电影让我深深感动，每次重看都有新的体会。', 'rating': 5})
r2, _ = Review.objects.get_or_create(user=user2, movie=movie2, defaults={'title': '最硬核的父爱', 'content': '诺兰用最宏大的宇宙叙事，讲了一个最朴素的关于爱的故事。当库珀在黑洞中看到女儿长大的那一幕，我泪流满面。科幻只是外壳，爱才是内核。', 'rating': 5})

Comment.objects.get_or_create(user=user2, review=r1, defaults={'content': '完全同意！这是我心中永远的No.1'})
Comment.objects.get_or_create(user=user1, review=r2, defaults={'content': '是的，诺兰真是太会讲故事了，五维空间那段太震撼了'})

Favorite.objects.get_or_create(user=user1, movie=movie1)
Favorite.objects.get_or_create(user=user1, movie=movie2)
Favorite.objects.get_or_create(user=user2, movie=movie2)

print('测试数据初始化完成!')
print(f'分类数: {Category.objects.count()}')
print(f'电影数: {Movie.objects.count()}')
print(f'影评数: {Review.objects.count()}')
print(f'评论数: {Comment.objects.count()}')
print(f'收藏数: {Favorite.objects.count()}')
print(f'\n管理员账号: admin / admin123')
print(f'测试用户: filmfan / 123456')
print(f'测试用户: movielover / 123456')
