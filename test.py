import numpy as np
import pandas as pd
import csv
import folium

class Place:

    def __init__(self, name, location, type, rating, operating_time , parking_available):
        self.name = name
        self.location = location
        self.type = type
        self.rating = rating
        self.operating_tiem = operating_time
        self.parking_available = parking_available


class Restaurant(Place):

    def __init__(self, name, location, type, rating, operating_time , parking_available, type_of_foods, rep_menu, avg_price):
        super().__init__(name, location, type, rating, operating_time , parking_available)
        self.types_of_foods = type_of_foods
        self.rep_menu = rep_menu
        self.avg_price = avg_price

    

class Cafe(Place):

    def __init__(self, name, location, type, rating, operating_time ,No_coffee, parking_available, rep_menu):
        super().__init__(name, location, type, rating, operating_time , parking_available)
        self.No_coffee = No_coffee
        self.rep_menu = rep_menu


class Entertainments(Place):

    def __init__(self, name, location, type, rating, operating_time , parking_available, performace_available, entertainments_info):
        super().__init__(name, location, type, rating, operating_time , parking_available)
        self.perforamance_available = performace_available
        self.entertainmets_info = entertainments_info
        

    

class Entertainment_Info:

    def __init__(self, timetable_info, price, for_inquiry):
        self.timetalbe = timetable_info
        self.price = price
        self.for_inquiry = for_inquiry

    def possible_time():
        file_path = 'test_for_term_project.csv'

        with open(file_path,newline = '') as csvfile:
            csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            print(row)
import csv
from geopy.distance import geodesic
from math import inf
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

        num = 0

        if "식사" in separted_date:
            food_type = input("원하는 음식 종류를 입력해주세요.(space bar가 포함되면 안 됩니다.)(선택지 : 한식, 양식, 중식, 일식)\nex)양식")
            price_limit = int(input("음식 평균 가격 상한선을 입력해주세요(space bar가 포함되면 안 됩니다.)\nex)30000"))
            Restaurants = list()

            with open(file_path_food, newline='') as csvfile:
                Collection_restaurant = csv.reader(csvfile)
                Collection_restaurant.__next__()
                for info in Collection_restaurant:
                    
                    info[1] = info[1].split(',')
                    info[1] = (float(info[1][0]), float(info[1][1]))
                    Restaurants.append(Restaurant(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8]))
                    
            num +=1
                    
        
        
        if "놀거리" in separted_date:
            p = input("주차 필요하신가요?(선택지 : Yes or No)\nex)Yes")
            if p == "Yes":
                parking_available = True
            else:
                parking_available = False
            Doing_funs = list()

            with open(file_path_doing_fun, newline='') as csvfile:
                Collection_doing_fun = csv.reader(csvfile)
                Collection_doing_fun.__next__()
                for info in Collection_doing_fun:
                    info[1] = info[1].split(',')
                    info[1] = (float(info[1][0]), float(info[1][1]))
                    Doing_funs.append(Entertainments(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7]))
            num +=1

        if "카페" in separted_date:
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
                    Cafes.append(Cafe(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7]))
            num +=1

        Full_course_candidates = [ [["A","a"],inf],[["B","b"],inf],[["C","c"],inf],[["D","d"],inf],[["E","e"],inf]]

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

            for i in range(len(separted_date)-1):
                Collection_place_now = dict()
                Collection_place_next = dict()

                match separted_date[i]:
                    case "식사":
                        match separted_date[i+1]:
                            case "식사":
                                for place_now in Restaurants:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Restaurants:
                                    Collection_place_next[place_next.name] = place_next.location
                                
                            case "카페":
                                for place_now in Restaurants:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Cafes:
                                    Collection_place_next[place_next.name] = place_next.location
                            case "놀거리":
                                for place_now in Restaurants:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Doing_funs:
                                    Collection_place_next[place_next.name] = place_next.location

                    case "카페":
                        match separted_date[i+1]:
                            case "식사":
                                for place_now in Cafes:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Restaurants:
                                    Collection_place_next[place_next.name] = place_next.location
                            case "카페":
                                for place_now in Cafes:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Cafes:
                                    Collection_place_next[place_next.name] = place_next.location
                            case "놀거리":
                                for place_now in Cafes:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Doing_funs:
                                    Collection_place_next[place_next.name] = place_next.location

                    case "놀거리":
                        match separted_date[i+1]:
                            case "식사":
                                for place_now in Doing_funs:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Restaurants:
                                    Collection_place_next[place_next.name] = place_next.location
                            case "카페":
                                for place_now in Doing_funs:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Cafes:
                                    Collection_place_next[place_next.name] = place_next.location
                            case "놀거리":
                                for place_now in Doing_funs:
                                    Collection_place_now[place_now.name] = place_now.location
                                for place_next in Doing_funs:
                                    Collection_place_next[place_next.name] = place_next.location


                distance_bet_places = dict()
                for place_now in Collection_place_now:
                    dist_candidate = dict()
                    for place_next in Collection_place_next:
                        dist_candidate[place_next] = geodesic(Collection_place_now[place_now],Collection_place_next[place_next]).meters

                    distance_bet_places[place_now] = dist_candidate
                
                for place in distance_bet_places:
                    present_place, next_places = (place, distance_bet_places[place])
                    if i ==0:
                        for candidate in next_places:
                            for idx in range(5):
                                if(next_places[candidate]<Full_course_candidates[idx][-1]):
                                    if idx<4:
                                        Full_course_candidates[idx+1] = Full_course_candidates[idx]
                                    
                                    Full_course_candidates[idx][0][0] = present_place
                                    Full_course_candidates[idx][0][1] = candidate
                                    Full_course_candidates[idx][-1] = next_places[candidate]
                                    break


                    else:
                        candidate_for_appending_Full_course = [ [["A","a"],inf],[["B","b"],inf],[["C","c"],inf],[["D","d"],inf],[["E","e"],inf],[["F","f"],inf],[["G","g"],inf],[["H","h"],inf],[["I","i"],inf],[["J","j"],inf]]
                        
                        for index in range(5):
                            if present_place == Full_course_candidates[index][0][-1]:
                                for candidate in next_places:
                                    for idx in range(10):
                                        if(next_places[candidate]<candidate_for_appending_Full_course[idx][-1]):
                                            if idx<9:
                                                candidate_for_appending_Full_course[idx+1] = candidate_for_appending_Full_course[idx]

                                            candidate_for_appending_Full_course[idx][0][0] = present_place
                                            candidate_for_appending_Full_course[idx][0][1] = candidate
                                            candidate_for_appending_Full_course[idx][-1] = next_places[candidate]
                                            break
                            
                            for CANDIDATE in candidate_for_appending_Full_course:
                                for index in range(5):
                                    if Full_course_candidates[index][0][-1] in CANDIDATE[0][0] and CANDIDATE[0][1] not in Full_course_candidates[index][0][:-1]:
                                        Full_course_candidates[index][0].append(CANDIDATE[0][1])
                                        Full_course_candidates[index][1] += CANDIDATE[1]


        for Course in Full_course_candidates:
            Course[1] = Course[1]/50  #3km/h => 50m/s로 움직이는 것. 이에 기반하여, 거리를 시간으로 변경함.


        df = pd.DataFrame(Full_course_candidates, columns=['데이트 코스','총 경과시간(분)(3km/h기준)'])
        max_len = df['데이트 코스'].str.len().max()
        df["데이트 코스"] = df["데이트 코스"].apply(' -> '.join)
        df['데이트 코스'] = df["데이트 코스"].apply(lambda x: x.ljust(max_len))
        print(df)


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

        colors = ['red', 'blue', 'green', 'orange', 'purple']

        MAP = folium.Map(location=(37.557434302, 126.926960224 ), zoom_start=6)  #홍대입구역을 기준으로 함. csv파일 속 위치들도 홍대 근처로 잡을 예정

        for (name, route), color in zip(routes.items(), colors):
            folium.PolyLine(locations=route, color = color).add_to(MAP)

        for i, (name, route) in enumerate(routes.items()):
            for j, coord in enumerate(route):
                rep = f"{name} - {j+1}번째 위치"
                match separted_date[i]:
                    case "식사":
                        rep += " (식당)"

                    case "카페":
                        rep += " (카페)"

                    case "놀거리":
                        rep += " (놀거리)"

                folium.Marker(location=coord, tooltip=rep)


        MAP  # map API 사용하여 위치 정보들과 경로들 시각화함.
        
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

                case _:
                    req_detail = input("잘못 입력하셨습니다. 다시 입력해주세요! \n몇 번째 추천 경로의 위치 정보들을 더 자세히 보고 싶으신가요?(공백 없이 입력해주세요!) \n(2번째 추천 경로를 상세히 보고 싶다면) ex)2  \n-------------------  \n⋇종료를 원하시면, ex)종료 \n: ")
            
            idx = 1
            for place in Details:
                rep = "     "
                rep += str(idx)+"번째 위치 정보 : "+"이름 : {:}, 분류 : {:}, 평점 : {:}, 운영시간 : {:}".format(place.name, place.type, place.rating, place.operating_tiem)
                match place.type:
                    case "식당":
                        rep += "음식 종류 : {:}, 대표메뉴 : {:}, 평균가 : {:}".format(place.types_of_foods, place.rep_menu, place.avg_price)

                    case "카페":
                        rep += "커피 말고 마실 만한 메뉴가 있는 지 : {:}, 대표메뉴 : {:}".format(place.No_coffee, place.rep_menu)

                    case "놀거리":
                        rep += "공연 여부 : {:}, 공연 정보 : {:}".format(place.perforamance_available, place.entertainments_info)
                

                print(rep)
                print()

                idx += 1




        

        
        command = input("다시 시작하기를 원하신다면 '시작'을, 종료를 원하신다면 '종료'를 입력해주세요! \n ex)종료 \n: ")