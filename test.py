import numpy as np
import pandas as pd
import csv

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
""""

try exception 구문 별로 잘못됐을 때 보강 하는 거 짜기

"""

if __name__ == "__main__":
    
        date = input("원하는 데이트 코스를 입력해주세요.(space bar가 포함되면 안 됩니다.)(선택지 : 식사, 카페, 놀거리)\n ex)식사->카페->놀거리->카페")
        separted_date = date.split('->')
        
        file_path_food = 'Place_food.csv'
        file_path_cafe = 'Place_cafe.csv'
        file_path_doing_fun = 'Place_doing_fun.csv'

        if "식사" in separted_date:
            food_type = input("원하는 음식 종류를 입력해주세요.(space bar가 포함되면 안 됩니다.)(선택지 : 한식, 양식, 중식, 일식)\nex)양식")
            price_limit = int(input("음식 평균 가격 상한선을 입력해주세요(space bar가 포함되면 안 됩니다.)\nex)30000"))
            Restaurants = list()

            with open(file_path_food, newline='') as csvfile:
                Collection_restaurant = csv.reader(csvfile)
                Collection_restaurant.__next__()
                for info in Collection_restaurant:
                    if(int(info[8])<price_limit):
                        info[1] = info[1].split(',')
                        info[1] = (float(info[1][0]), float(info[1][1]))
                        Restaurants.append(Restaurant(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8]))
                    else:
                        del info
                    
        
        
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


        now = separted_date[0]
        separted_date = separted_date[1:]

        Full_course_candidates = [[[],0],[[],0],[[],0],[[],0],[[],0]]
        cnt = 1

        for Next in separted_date:
            Collection_place_now = dict()
            Collection_place_next = dict()
            Collection_place_second = dict()

            match now:
                case "식사":
                    for place in Restaurants:
                        Collection_place_now[place.name] = place.location

                case "카페":
                    for place in Cafes:
                        Collection_place_now[place.name] = place.location

                case "놀거리":
                    for place in Doing_funs:
                        Collection_place_now[place.name] = place.location

            match Next:
                case "식사":
                    for place in Restaurants:
                        Collection_place_next[place.name] = place.location

                case "카페":
                    for place in Cafes:
                        Collection_place_next[place.name] = place.location

                case "놀거리":
                    for place in Doing_funs:
                        Collection_place_next[place.name] = place.location

            #현재 위치한 곳의 위치에서 다음에 갈 곳(Collection_place_next)까지의 거리를 모두 구해서 dictionary에 넣어놓기(Greedy Algorithm 사용 위함)
            #시간 복잡도가 expotential함. 그리디 알고리즘 말고 다른 방안 모색해보기.
            # => 최근접이웃 알고리즘으로 대체. 경로가 짧지 않을 수 있기에, path 후보군 5개를 계속 가져감.
            distance_bet_places = dict()
            for place_now in Collection_place_now:
                dist_candidate = dict()
                for place_next in Collection_place_next:
                    dist_candidate[place_next] = geodesic(Collection_place_now[place_now],Collection_place_next[place_next]).meters
                
                distance_bet_places[place_now] = dist_candidate

            candidate_for_appending_Full_course = [ ["A",-1],["B",-1],["C",-1],["D",-1],["E",-1],["F",-1],["G",-1],["H",-1],["I",-1],["J",-1]]
            for place in distance_bet_places:
                present_place, next_places = place.items()
                if cnt ==1:
                    for idx in range(10):
                        if(candidate.value()<candidate_for_appending_Full_course[idx][-1]):
                            if idx<10:
                                candidate_for_appending_Full_course[idx+1] = candidate_for_appending_Full_course[idx]

                            candidate_for_appending_Full_course[idx] = [str(list(candidate.keys())),candidate.values()]
                            break

                    for i in range(5):
                        Full_course_candidates[i] = candidate_for_appending_Full_course[i]

                elif present_place == Full_course_candidates[0][-1]:

                    for candidate in next_places:
                        for idx in range(10):
                            if(candidate.value()<candidate_for_appending_Full_course[idx][-1]):
                                if idx<10:
                                    candidate_for_appending_Full_course[idx+1] = candidate_for_appending_Full_course[idx]

                                candidate_for_appending_Full_course[idx] = [str(list(candidate.keys())),candidate.values()]
                                break

                    for CANDIDATE in candidate_for_appending_Full_course:
                        for index in range(5):
                            if Full_course_candidates[index][0][-1] in CANDIDATE:
                                Full_course_candidates[index][0].append(CANDIDATE[0])
                                Full_course_candidates[index][1] += CANDIDATE[1]

            cnt += 1

        print(Full_course_candidates) #테스트용

        """
        
        #What I have to do
        1. 추가적인 기능들 구현하기(표 형식으로 깔끔하게 올린다든지, No_coffee(Cafe)라는 거 반영하는 등)
        2. csv파일 채우기 각 10개 이상씩 우리 동네 네이버지도 베끼면서

        
        """
                       



            
            
        
    

    