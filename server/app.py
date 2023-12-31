from flask import Flask, render_template, request
import pandas as pd
import csv
from geopy.distance import geodesic

app = Flask(__name__)

# 이전 코드에서 데이터 및 클래스 정의 등이 포함된 부분

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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



        date = request.form["date_course"]
        separted_date = date.split('->')
                    
        file_path_food = 'Place_food.csv'
        file_path_cafe = 'Place_cafe.csv'
        file_path_doing_fun = 'Place_doing_fun.csv'


        food_type = request.form['food_type']
        price_limit = request.form['price_limit']
        Restaurants = list()

        with open(file_path_food, newline='') as csvfile:
            Collection_restaurant = csv.reader(csvfile)
            Collection_restaurant.__next__()
            for info in Collection_restaurant: 
                info[1] = info[1].split(',')
                info[1] = (float(info[1][0]), float(info[1][1]))
                Restaurants.append(Restaurant(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8]))
                                
                    
                    

        p = request.form['parking_needed']
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

        # Full_course_candidates = [ [["A","a"],inf],[["B","b"],inf],[["C","c"],inf],[["D","d"],inf],[["E","e"],inf]]
        Full_course_candidates =list()
        num = len(separted_date)
                    
        if num>1:
            dist_from_food_to_cafe = dict()
            dist_from_food_to_doing_fun = dict()
            dist_from_food_to_food = dict()

            dist_from_cafe_to_food = dict()
            dist_from_cafe_to_doing_fun = dict()
            dist_from_cafe_to_cafe = dict()

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


                for i in range(5):
                    Full_course_candidates[i][1] = Full_course_candidates[i][1]/50  #3km/h => 50m/s로 움직이는 것. 이에 기반하여, 거리를 시간으로 변경함.
                df = pd.DataFrame(Full_course_candidates, columns=['데이트 코스','예상 경과시간(도보 3km/h 기준)'], index=['1번째 추천', '2번째 추천','3번째 추천','4번째 추천','5번째 추천'])
                max_len = df['데이트 코스'].str.len().max()
                df["데이트 코스"] = df["데이트 코스"].apply(' -> '.join)
                df['데이트 코스'] = df["데이트 코스"].apply(lambda x: x.ljust(max_len))


        return render_template('result.html', result=df)  # 결과를 result.html 템플릿에 넘겨줍니다.
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
