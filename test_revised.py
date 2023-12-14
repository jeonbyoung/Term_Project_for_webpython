import pandas as pd
import csv
from geopy.distance import geodesic
import folium
import webbrowser

class Place:

    def __init__(self, name, location, type, rating, operating_time):
        self.name = name
        self.location = location
        self.type = type
        self.rating = rating
        self.operating_tiem = operating_time


class Restaurant(Place):

    def __init__(self, name, location, type, rating, operating_time, type_of_foods, rep_menu, avg_price):
        super().__init__(name, location, type, rating, operating_time)
        self.types_of_foods = type_of_foods
        self.rep_menu = rep_menu
        self.avg_price = avg_price

    

class Cafe(Place):

    def __init__(self, name, location, type, rating, operating_time,no_coffee_possible,rep_menu):
        super().__init__(name, location, type, rating, operating_time)
        self.no_coffee_possible = no_coffee_possible
        self.rep_menu = rep_menu


class Entertainments(Place):

    def __init__(self, name, location, type, rating, operating_time, performace_available, entertainments_info):
        super().__init__(name, location, type, rating, operating_time)
        self.perforamance_available = performace_available
        self.entertainments_info = entertainments_info
        

def make_Full_course(i,distance_bet_places,Full_course_candidates):
    l = list()
    if i ==0:
        for place in distance_bet_places:
            present_place, next_places = (place, distance_bet_places[place])
            for candidate in next_places:         
                for candidate in next_places:
                    if next_places[candidate] != 0:
                        l.append([[present_place,candidate],next_places[candidate]])

        l.sort(key=lambda x: x[1])
        idx = 1
        var = l[0][0][0]
        while len(Full_course_candidates)<5:
            if l[idx][0][0] != var:
                Full_course_candidates.append(l[idx])
                var = l[idx][0][0]
            idx +=1


    else:
        for place in distance_bet_places:
            present_place, next_places = (place, distance_bet_places[place])
            for path in Full_course_candidates:
                for candidate in next_places:
                    if path[0][-1] == present_place:
                        l.append([[present_place,candidate],next_places[candidate]])
        l.sort(key=lambda x: x[1])

        for path in Full_course_candidates:
            for sub_path in l:
                if sub_path[0][0]==path[0][-1] and sub_path[0][1] not in path[0]:
                    path[0].append(sub_path[0][1])
                    path[1] += sub_path[1]
            
    return Full_course_candidates

def distance_bet_places(Collection_place_now,Collection_place_next):
    distance_bet_places = dict()
    for place_now in Collection_place_now:
        dist_candidate = dict()
        for place_next in Collection_place_next:
            dist_candidate[place_next] = geodesic(Collection_place_now[place_now],Collection_place_next[place_next]).meters
        distance_bet_places[place_now] = dist_candidate

    return distance_bet_places

""""

try exception 구문 별로 잘못됐을 때 보강 하는 거 짜기

"""

if __name__ == "__main__":
    command = input("안녕하세요! 시작을 원하시면 '시작'을, 종료하시려면 '종료'를 입력해주세요! \n")
    while(command!="종료"):
        date = input("원하는 데이트 코스를 입력해주세요.(space bar가 포함되면 안 됩니다.)(선택지 : 식사, 카페, 놀거리)\n ex)식사->카페->놀거리->카페")
        separted_date = date.split('->')
        
        file_path_food = 'Place_food.csv'
        file_path_cafe = 'Place_cafe.csv'
        file_path_doing_fun = 'Place_doing_fun.csv'
      
        Restaurants = list()

        with open(file_path_food, newline='') as csvfile:
            Collection_restaurant = csv.reader(csvfile)
            Collection_restaurant.__next__()
            for info in Collection_restaurant: 
                info[1] = info[1].split(',')
                info[1] = (float(info[1][0]), float(info[1][1]))
                Restaurants.append(Restaurant(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7]))
                    
        
        Doing_funs = list()

        with open(file_path_doing_fun, newline='') as csvfile:
            Collection_doing_fun = csv.reader(csvfile)
            Collection_doing_fun.__next__()
            for info in Collection_doing_fun:
                info[1] = info[1].split(',')
                info[1] = (float(info[1][0]), float(info[1][1]))
                Doing_funs.append(Entertainments(info[0],info[1],info[2],info[3],info[4],info[5],info[6]))


        p = input("커피 못 드시나요?(선택지 : Yes or No)\nex)Yes")
        if p == "Yes":
            coffee = False
        else:
            coffee = True
        
        Cafes = list()

        with open(file_path_cafe, newline='') as csvfile:
            Collection_cafe = csv.reader(csvfile)
            Collection_cafe.__next__()
            for info in Collection_cafe:
                info[1] = info[1].split(',')
                info[1] = (float(info[1][0]), float(info[1][1]))
                Cafes.append(Cafe(info[0],info[1],info[2],info[3],info[4],info[5],info[6]))

        Full_course_candidates =list()
        num = len(separted_date)
        
        if num>1:
            dist_from_food_to_cafe = dict()
            dist_from_food_to_doing_fun = dict()
            dist_from_food_to_food = dict()

            dist_from_cafe_to_food = dict()
            dist_from_cafe_to_doing_fun = dict()
            dist_fromm_cafe_to_cafe = dict()

            dist_from_doing_fun_to_food = dict()
            dist_from_doing_fun_to_cafe = dict()
            dist_from_doing_fun_to_doing_fun = dict()


            for i in [Restaurants, Cafes, Doing_funs]:
                for j in [Restaurants, Cafes, Doing_funs]:
                    Collection_place_now = dict()
                    Collection_place_next = dict()

                    for places_now in i:
                        Collection_place_now[places_now.name] = places_now.location
                    for places_next in j:
                        Collection_place_next[places_next.name] = places_next.location

                    if i == Restaurants:
                        if j == Restaurants:
                            dist_from_food_to_food = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Cafes:
                            dist_from_food_to_cafe = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Doing_funs:
                            dist_from_food_to_doing_fun = distance_bet_places(Collection_place_now,Collection_place_next)

                    if i == Cafes:
                        if j == Restaurants:
                            dist_from_cafe_to_food = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Cafes:
                            dist_from_cafe_to_cafe = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Doing_funs:
                            dist_from_cafe_to_doing_fun = distance_bet_places(Collection_place_now,Collection_place_next)
                    if i == Doing_funs:
                        if j == Restaurants:
                            dist_from_doing_fun_to_food = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Cafes:
                            dist_from_doing_fun_to_cafe = distance_bet_places(Collection_place_now,Collection_place_next)
                        if j == Doing_funs:
                            dist_from_doing_fun_to_doing_fun = distance_bet_places(Collection_place_now,Collection_place_next)


            for i in range(len(separted_date)-1):
                Collection_place_now = dict()
                Collection_place_next = dict()

                match separted_date[i]:
                    case "식사":
                        match separted_date[i+1]:
                            case "식사":
                                Full_course_candidates = make_Full_course(i,dist_from_food_to_food,Full_course_candidates)
                            case "카페":
                                Full_course_candidates = make_Full_course(i,dist_from_food_to_cafe,Full_course_candidates)
                            case "놀거리":
                                Full_course_candidates = make_Full_course(i,dist_from_food_to_doing_fun,Full_course_candidates)

                    case "카페":
                        match separted_date[i+1]:
                            case "식사":
                                Full_course_candidates = make_Full_course(i,dist_from_cafe_to_food,Full_course_candidates)
                            case "카페":
                                Full_course_candidates = make_Full_course(i,dist_from_cafe_to_cafe,Full_course_candidates)
                            case "놀거리":
                                Full_course_candidates = make_Full_course(i,dist_from_cafe_to_doing_fun,Full_course_candidates)

                    case "놀거리":
                        match separted_date[i+1]:
                            case "식사":
                                Full_course_candidates = make_Full_course(i,dist_from_doing_fun_to_food,Full_course_candidates)
                            case "카페":
                                Full_course_candidates = make_Full_course(i,dist_from_doing_fun_to_cafe,Full_course_candidates)
                            case "놀거리":
                                Full_course_candidates = make_Full_course(i,dist_from_doing_fun_to_doing_fun,Full_course_candidates)



            df = pd.DataFrame(Full_course_candidates, columns=['데이트 코스','예상 도보 시간(분)(3km/h기준)'], index=['1번째 추천 : ', '2번째 추천 : ','3번째 추천 : ','4번째 추천 : ','5번째 추천 : '])
            max_len = df['데이트 코스'].str.len().max()
            df["데이트 코스"] = df["데이트 코스"].apply(' -> '.join)
            df['데이트 코스'] = df["데이트 코스"].apply(lambda x: x.ljust(max_len))

            print(df)

            for Course in Full_course_candidates:
                Course[1] = Course[1]/50  #3km/h => 50m/s로 움직이는 것. 이에 기반하여, 거리를 시간으로 변경함.

            routes = dict()
            n = 1
            for Course in Full_course_candidates:
                line = list()
                for idx in range(len(Course[0])):
                    match separted_date[idx]:
                        case "식사":
                            for restaurant in Restaurants:
                                if restaurant.name == Course[0][idx]:
                                    Course[0][idx] = restaurant

                        case "카페":
                            for cafe in Cafes:
                                if cafe.name == Course[0][idx]:
                                    Course[0][idx] = cafe

                        case "놀거리":
                            for doing_fun in Doing_funs:
                                if doing_fun.name == Course[0][idx]:
                                    Course[0][idx] = doing_fun

                    line.append(Course[0][idx].location)
                rep = str(n)+"번째 추천 경로"
                routes[rep] = line
                n+=1

            colors = ['red', 'blue', 'green', 'orange', 'purple']

            M = folium.Map(location=routes['1번째 추천 경로'][0], zoom_start=9)  #1번째 추천 경로의 첫 번째 위치를 기준으로 함.

            for (name, route), color in zip(routes.items(), colors):
                folium.PolyLine(locations=route, color = color).add_to(M)

            for i, (name, route) in enumerate(routes.items()):
                for j, coord in enumerate(route):
                    rep = f"{name} - {j+1}번째 위치"
                    match separted_date[j]:
                        case "식사":
                            rep += " (식당)"

                        case "카페":
                            rep += " (카페)"

                        case "놀거리":
                            rep += " (놀거리)"

                    folium.Marker(location=coord, tooltip=rep).add_to(M)


            M.save("map.html")  # map API 사용하여 위치 정보들과 경로들 시각화함.
            webbrowser.open("map.html")

            req_detail = "0"
            
            while(req_detail != "종료"):
                req_detail = input("몇 번째 추천 경로의 위치 정보들을 더 자세히 보고 싶으신가요?(공백 없이 입력해주세요!) \n(2번째 추천 경로를 상세히 보고 싶다면) ex)2  \n-------------------  \n⋇종료를 원하시면, ex)종료 \n: ")
                match req_detail:
                    case "1":
                        Details = Full_course_candidates[int(req_detail)][0]

                    case "2":
                        Details = Full_course_candidates[int(req_detail)][0]

                    case "3":
                        Details = Full_course_candidates[int(req_detail)][0]

                    case "4":
                        Details = Full_course_candidates[int(req_detail)][0]

                    case "5":
                        Details = Full_course_candidates[int(req_detail)][0]

                    case "종료":
                        break

                    case _:
                        req_detail = input("잘못 입력하셨습니다. 다시 입력해주세요! \n몇 번째 추천 경로의 위치 정보들을 더 자세히 보고 싶으신가요?(공백 없이 입력해주세요!) \n(2번째 추천 경로를 상세히 보고 싶다면) ex)2  \n-------------------  \n⋇종료를 원하시면, ex)종료 \n: ")
                        continue
                
                print("-----------------------------------------------------")
                print(req_detail+"번째 추천 경로에 대한 추가 정보들입니다!")
                print("-----------------------------------------------------\n")

                idx = 1
                for place in Details:
                    rep = "     "
                    rep += str(idx)+"번째 위치 정보 : "+"이름 : {:}, 분류 : {:}, 평점 : {:}, 운영시간 : {:}, ".format(place.name, place.type, place.rating, place.operating_tiem)
                    match place.type:
                        case "식당":
                            rep += "음식 종류 : {:}, 대표메뉴 : {:}, 평균가 : {:}".format(place.types_of_foods, place.rep_menu, place.avg_price)

                        case "카페":
                            rep += "커피 말고 마실 만한 메뉴가 있는 지 : {:}, 대표메뉴 : {:}".format(place.no_coffee_possible, place.rep_menu)

                        case "놀거리":
                            rep += "공연 여부 : {:}, 공연 정보 : {:}".format(place.perforamance_available, place.entertainments_info)
                    

                    print(rep)
                    print()

                    idx += 1

                print("-"*100)
                print()
                
            command = input("다시 시작하기를 원하신다면 '시작'을, 종료를 원하신다면 '종료'를 입력해주세요! \n ex)종료")
        else:
            print("한 개 이상의 장소를 입력하셔야합니다!")
                


                