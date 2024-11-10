import random

BOARD_WIDTH = 8
BOARD_HEIGHT = 7
ITEMS = ["L", "B", "S"]

cat_items = []

class Mouse:
    def __init__(self):
        self.position = [5, 6]
        self.vision_range = 2
        self.loophole_usage = 2
        self.loopholes = {
            (1, 0): [(1, 6), (5, 1), (5, 6)],
            (1, 7): [(1, 1), (5, 1), (5, 6)],
            (5, 0): [(1, 1), (1, 6), (5, 6)],
            (5, 7): [(1, 1), (1, 6), (5, 1)]
        }
        self.destination = self.find_second_closest_loophole()
        self.vision_board = self.create_vision_board()

    def create_vision_board(self, vision_range=2):
        vision_board = [[False for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        for dx in range(-vision_range, vision_range + 1):
            for dy in range(-vision_range, vision_range + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH:
                    vision_board[x][y] = True
        return vision_board

    def update_vision_board(self):
        self.vision_board = self.create_vision_board()

    def find_closest_loophole(self):
        distances = sorted(
            [(abs(self.position[0] - x) + abs(self.position[1] - y), (x, y))
             for (x, y) in self.loopholes.keys()]
        )
        return distances[0][1]

    def find_second_closest_loophole(self):
        distances = sorted(
            [(abs(self.position[0] - x) + abs(self.position[1] - y), (x, y))
             for (x, y) in self.loopholes.keys()]
        )
        return distances[1][1] if len(distances) > 1 else distances[0][1]

    def move_towards_destination(self):
        dx = self.destination[0] - self.position[0]
        dy = self.destination[1] - self.position[1]

        if abs(dx) >= abs(dy):
            new_x = self.position[0] + (1 if dx > 0 else -1)
            if 0 < new_x < BOARD_HEIGHT:
                self.position[0] = new_x
        else:
            new_y = self.position[1] + (1 if dy > 0 else -1)
            if 0 < new_y < BOARD_WIDTH:
                self.position[1] = new_y

        if self.position == self.destination:
            self.use_loophole()

    def use_loophole(self):
        pos = (self.position[0], self.position[1])
        if self.loophole_usage > 0 and pos in self.loopholes:
            print("抜け穴を使用しました！")
            self.loophole_usage -= 1
            selected_exit = random.choice(self.loopholes[pos])
            self.position = list(selected_exit)

    def use_loophole_if_nearby(self, cat_position):
        if tuple(self.position) in self.loopholes:
            self.loophole_usage -= 1
            exits = self.loopholes[tuple(self.position)]
            farthest_exit = max(
                exits, key=lambda e: abs(cat_position[0] - e[0]) + abs(cat_position[1] - e[1])
            )
            self.position = list(farthest_exit)
            print(f"抜け穴を使用して移動: 新しい位置 {self.position}")
        else:
            print("入れないんじゃない。入らないだけだ。")

    def update_destination_if_cat_nearby(self):
        closest_loophole = self.find_closest_loophole() # 2番目に近い穴
        if closest_loophole != self.position:
            print(f"ねこが視界に入ったため、目的地を最も近い抜け穴 {closest_loophole} に変更しました")
        self.destination = closest_loophole

    def auto_move(self, cat_position):
        self.update_vision_board()
        print(self.position) # てすと！！！!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if self.is_cat_in_vision(cat_position):
            print(f"ねこが視界に入った！位置: {cat_position}")
            self.update_destination_if_cat_nearby()
            self.move_towards_destination()# 目的地に向かって移動させる
            self.use_loophole()# 必要であれば抜け穴を使用

        else:
            print("いどうちゅ～")
            self.move_towards_destination()
            self.use_loophole()
            print(f"現在の位置: {self.position}")

    def random_move(self):
        x, y = self.position
        possible_moves = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < BOARD_HEIGHT - 1 and 0 <= y + dy < BOARD_WIDTH - 1
        ]
        if possible_moves:
            self.position = list(random.choice(possible_moves))
            print(f"バケツ効果でランダム移動しました: 新しい位置 {self.position}")

    def is_cat_in_vision(self, cat_position):
        mouse_x, mouse_y = self.position
        cat_x, cat_y = cat_position
        return abs(mouse_x - cat_x) <= self.vision_range and abs(mouse_y - cat_y) <= self.vision_range

    # ネズミ手動バージョン
    # def mouse_move(self, direction): #ねずみの移動先決定
    #     x, y = self.position
    #     direction_map = {"W":(-1, 0),"A":(0,-1), "S":(1,0), "D":(0,1)}
    #     if direction in direction_map:
    #         dx, dy = direction_map[direction]
    #         nx, ny = x + dx, y + dy
    #         if 0 < nx < BOARD_HEIGHT-1 and 0 < ny < BOARD_WIDTH-1:
    #             if (nx, ny) not in self.loopholes:
    #                 self.position = [nx, ny]
    #             elif self.loophole_usage > 0:
    #                 # 抜け穴の使用回数があるなら、抜け穴を使用
    #                 self.use_loophole(nx, ny)
    #             else:
    #                 print("抜け穴はもう使用できません")
    #                 self.mouse_move(input("ネズミの移動 (WASD): ").upper())
    #         elif (nx, ny) in self.loopholes:
    #             self.use_loophole(nx, ny)
    #         else:
    #             print("行き止まりです")
    #             self.mouse_move(input("ネズミの移動 (WASD): ").upper())

        

class Cat:  #ネコ(プレイヤー)の管理
    def __init__(self):
        self.position = [1, 1]  # 初期位置
        self.items = {'L': 10, 'B': 10, 'S': 10}  # 所持しているアイテムリスト
        self.extra_moves = 1
        self.mouse = Mouse()
        self.item = Item(cat_items)
        
    def next_move(self, direction, mouse_position, item_position, item_type):#ネコの移動先決定
        input_flag = True
        x, y = self.position
        direction_map = {"Q":(-1, -1), "W":(-1, 0), "E":(-1,1),
                         "A":(0,-1), "D":(0,1),
                         "Z":(1,-1), "X":(1,0), "C":(1,1)}
        if direction in direction_map:
            dx, dy = direction_map[direction]
            for hosuu in range(self.extra_moves):
                nx, ny = x + dx, y + dy
                print(nx,ny)
                if 0 < nx < BOARD_HEIGHT-1 and 0 < ny < BOARD_WIDTH-1:
                    self.position = [nx, ny]
                    if check_win(self.position, mouse_position):
                        break
                    if check_get_item(self.position, item_position):
                        print(f'{item_type}をゲット！')
                        self.items[item_type] += 1 
                        item_position = [None, None] 
                    x, y = nx, ny  # 更新された位置を次のステップの基準に
                else:
                    if hosuu == 0:
                        print("行き止まりDA★")
                        while input_flag:
                            next_cat = input("ネコの移動 (QWEADZXC): ").upper()  # ボードの外に出る場合は移動を停止
                            if next_cat not in ["Q","W","E","A","D","Z","X","C"]:
                                print("入力が適切ではありません。")
                            else:
                                input_flag = False
                            self.next_move(next_cat, mouse_position, item_position, item_type)
                    else:
                        self.extra_moves = 1
                        return
            if self.extra_moves == 3:
                self.extra_moves = 1

    def use_item(self, game_board):  # アイテム使用処理
        while True:
            available_items = {can_use: count for can_use, count in self.items.items() if count > 0}
            if not available_items:
                print("アイテムを所持してません")
                return False, []
            print(f"所持アイテム: {available_items}")
            choice = input("アイテムを使用(1:懐中電灯(L), 2:バケツ(B), 3:シューズ(S)), 4:キャンセル>>>")

            try:
                choice = int(choice)
                if choice in [1, 2, 3, 4]:
                    if choice == 4:
                        print("アイテムの使用をキャンセルしました")
                        return False, []
                    item_keys = list(self.items.keys())
                    selected_item = item_keys[choice - 1]
                    if self.items[selected_item] > 0:
                        self.items[selected_item] -= 1
                        print(f"{selected_item}を使いました！")
                        light_positions = self.item.apply_effect(self.position, selected_item, game_board)
                        if selected_item == "S":
                            self.extra_moves = 3
                            return False, light_positions
                        elif selected_item == "B":
                            return True, light_positions
                        elif selected_item == "L":
                            return False, light_positions
                        break
                    else:
                        print("そのアイテムを持っていない！")
                else:
                    print("無効な入力です。1から4の数字を入力してください。")
            except ValueError:
                print("無効な入力です。1~4の数字のみ入力してください。")
                
                    

class Item:  # アイテム3種の管理
    def __init__(self, cat_items, position=None):
        available_items = [item for item in ITEMS if item not in cat_items]
        if not available_items:
            available_items = ITEMS
        self.type = random.choice(available_items)
        if position is None:
            self.position = [3, 4]
        else:
            self.position = position
        
    def apply_effect(self, cat_position, item, game_board):
        print("こうかはつど～う")  # テスト
        if item == "L":
            light_dir = self.light_used()  # 方向を取得
            light_positions = self.get_light_positions(light_dir, cat_position, game_board)
            return light_positions
        return[]
            
    def light_used(self):
        light_dir = input("ライトをつかった！\n照らしたい方向を移動キーで選択(QWEADZXC):").upper()
        while light_dir not in ["Q", "W", "E", "A", "D", "Z", "X", "C"]:
            print("入力が正しくありません。もう一度入力してください。")
            light_dir = input("照らしたい方向を移動キーで選択(QWEADZXC):").upper()
        print(f'現在地から {light_dir} の方向が明るくなった！')
        return light_dir

    def get_light_positions(self, light_dir, cat_position, game_board):
        direction_map = {
            "Q": (-1, -1), "W": (-1, 0), "E": (-1, 1),
            "A": (0, -1), "D": (0, 1),
            "Z": (1, -1), "X": (1, 0), "C": (1, 1)
        }
        dx, dy = direction_map[light_dir]
        x, y = cat_position
        light_positions = []
        while 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH:
            light_positions.append((x, y))
            if game_board[x][y] == "#" or game_board[x][y] == "h":  # 壁に当たったら停止
                break
            x += dx
            y += dy
        return light_positions

                
                    


def make_board():
    return [["#" if i == 0 or j == 0 or i == BOARD_HEIGHT-1 or j == BOARD_WIDTH-1 else '.' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

def update_vision_board(game_board, vision_board, cat_position, mouse_position, item_position, active_player, loopholes, bucket_effect_active, light_effect_positions):
    if active_player == 'cat':
        vision_range = 1
        vision_center = cat_position
        other_position = mouse_position
        display_other = 'M'
    else:
        if bucket_effect_active:
            vision_range = 0
        else:
            vision_range = 2
        vision_center = mouse_position
        other_position = cat_position
        display_other = 'C'

    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            vision_board[i][j] = "X" # 隠しマス
            
    # 通常の視界範囲
    for i in range(max(0, vision_center[0] - vision_range), min(BOARD_HEIGHT, vision_center[0] + vision_range + 1)):
        for j in range(max(0, vision_center[1] - vision_range), min(BOARD_WIDTH, vision_center[1] + vision_range + 1)):
            vision_board[i][j] = game_board[i][j]
            if [i, j] == item_position:
                vision_board[i][j] = 'I'
            if [i, j] == other_position:
                vision_board[i][j] = display_other
            for loophole in loopholes:
                if [i, j] == list(loophole):
                    vision_board[i][j] = 'h'
                    
    # ライト効果の適用
    for x, y in light_effect_positions:
        if 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH:
            vision_board[x][y] = game_board[x][y]
            if [x, y] == other_position:
                vision_board[x][y] = display_other
            elif [x, y] == item_position:
                vision_board[x][y] = 'I'
            for loophole in loopholes:
                if [x, y] == list(loophole):
                    vision_board[x][y] = 'h'

    vision_board[vision_center[0]][vision_center[1]] = 'C' if active_player == 'cat' else 'M'

    return vision_board


def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def check_win(cat_position, mouse_position):
    return cat_position == mouse_position

def check_get_item(cat_position, item_position):
    return cat_position == item_position

def game_loop():
    game_board = make_board()  # ゲーム全体の状態を管理するマップ
    vision_board = make_board()  # プレイヤーに表示されるマップ
    mouse = Mouse()
    cat = Cat()
    item = Item(cat_items)
    turn_count = 0
    game_over = False  # ゲームの終了を管理するフラグ
    bucket_effect_active = False # バケツの管理フラグ
    light_effect_positions = []  # ライトの照らしたマスのリスト

    while turn_count < 31 and not game_over:  # ゲーム終了フラグを確認
        if turn_count % 2 == 1:
            # ネズミのターン
            active_player = 'mouse'            
        else:
            # ネコのターン
            active_player = 'cat'

        # ネコ、ネズミ、アイテムの位置を更新した表示マップを作成
        update_vision_board(game_board, vision_board, cat.position, mouse.position, item.position, active_player, mouse.loopholes, bucket_effect_active, light_effect_positions)
        print_board(vision_board)  

        if turn_count % 2 == 1:
            while True:
                if bucket_effect_active:
                    mouse.random_move()
                    bucket_effect_active = False
                    turn_count += 1
                    break
                else:
                    mouse.auto_move(cat.position)
                    turn_count += 1
                    print(f"残りのターン{15-int(turn_count/2)}")
                    break
                
                    # 手動バージョン
                    # mouse_move = input("ネズミの移動 (WASD): ").upper()
                    # if mouse_move in ["W","A","S","D"]:
                    #     mouse.mouse_move(mouse_move)
                    #     if check_win(cat.position, mouse.position):
                    #         print("勝利！ネズミが突っ込んできた！")
                    #         game_over = True  # ゲーム終了フラグを設定
                    #         break
                    #     turn_count += 1
                    #     print(f"残りのターン{15-int(turn_count/2)}")
                    #     break
                    # else:
                    #     print("入力が間違っていませんか？")
            
        else:
            bucket_effect_active, l_positions = cat.use_item(game_board)
            for positions in l_positions:
                light_effect_positions.append(positions)
            while True:
                cat_move = input("ネコの移動 (QWEADZXC): ").upper()
                if cat_move in ["Q","W","E","A","D","Z","X","C"]:
                    cat.next_move(cat_move, mouse.position, item.position, item.type)
                    if check_win(cat.position, mouse.position):
                        print("勝利！ネズミをつかまえた！")
                        game_over = True  # ゲーム終了フラグを設定
                    turn_count += 1
                    break
                else:
                    print("入力が間違っていませんか？")
    
    if not game_over:
        print("ネズミに逃げられてしまった...")  # ターン数に到達してもゲームが終了しない場合

def print_rule():
        print("=== ルール ===")
        # ターンについて
        print("～ ターンについて ～")
        print("15ターン以内にネズミを捕まえたらネコの勝利です！")
        print("1ターンに1マス移動が必要です。")
        print("")
        # 移動方法について
        print("～ 移動方法について ～")
        print("ネコの移動キー:\n↖q ↑w e↗\n←a s d→\n↙z ↓x c↘")
        print("ネズミの移動範囲は上下左右の4方向です。")
        print("")
        # アイテム使用について
        print("～ アイテム使用について ～")
        print("アイテムは、L=ライト,S=シューズ,B=バケツ の三種類\nゲーム開始時に部屋のどこかに1つ落ちているほか、\nネズミが抜け穴(マップ上の「h」)を使用するとランダムで1つ、\n使用された抜け穴の位置に生成されます。")
        print("☆ アイテムの使用方法 ☆\n     数字キーにて  1=ライト、2=シューズ、3=バケツ\n   を所持しているアイテムに応じて押してください。\nアイテム使用をキャンセルしたい場合は、数字キー 0 を押してください。")
        print("")
        # 視界範囲について
        print("～ 視界範囲について ～")
        print("ネコの視界:\n      〇 〇 〇\n      〇 Ｃ 〇\n      〇 〇 〇\n      Ｃをネコとすると〇が見える範囲となります。")
        print("")
        print("ネズミの視界:\n      〇 〇 〇 〇 〇\n      〇 〇 〇 〇 〇\n      〇 〇 Ｍ 〇 〇\n      〇 〇 〇 〇 〇\n      〇 〇 〇 〇 〇\n      Ｍをネズミとすると〇が見える範囲となります。")
        print("")
        # ゲーム開始
        print("それでは、ゲームスタート！")



if __name__ == "__main__":  #起動
    print_rule()
    game_loop()