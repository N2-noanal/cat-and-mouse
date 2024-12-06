import random

BOARD_WIDTH = 8
BOARD_HEIGHT = 7
ITEMS = ["L", "B", "S"]

cat_items = []



class Mouse:
    def __init__(self, item):
        self.item = item
        self.position = random.choice([[1, 6], [5, 6], [5, 2], [5, 3], [5, 4]])
        self.last_seen_cat_position = None  # 最後に視認した猫の位置
        self.vision_range = 2
        self.loophole_usage = 2
        self.loopholes = {
            (1, 0): [(1, 6), (5, 1), (5, 6)],
            (1, 7): [(1, 1), (5, 1), (5, 6)],
            (5, 0): [(1, 1), (1, 6), (5, 6)],
            (5, 7): [(1, 1), (1, 6), (5, 1)],
        }
        self.destination = self.find_second_closest_loophole()
        self.vision_board = self.create_vision_board()

    def create_vision_board(self):
        """
        ネズミの視界範囲を計算してボード上に反映
        """
        vision_board = [[False for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH:
                    vision_board[x][y] = True
        return vision_board

    def find_closest_loophole(self):
        """
        一番近い抜け穴を探す
        """
        distances = sorted(
            [(abs(self.position[0] - x) + abs(self.position[1] - y), (x, y))
             for (x, y) in self.loopholes.keys()]
        )
        return distances[0][1]

    def find_second_closest_loophole(self):
        """
        二番目に近い抜け穴を探す
        """
        distances = sorted(
            [(abs(self.position[0] - x) + abs(self.position[1] - y), (x, y))
             for (x, y) in self.loopholes.keys()]
        )
        return distances[1][1] if len(distances) > 1 else distances[0][1]

    def is_within_bounds(self, x, y):
        """
        移動可能範囲の判定（抜け穴も考慮）
        """
        if 1 <= x <= 5 and 1 <= y <= 6:
            return True
        if (x, y) in self.loopholes.keys() and self.loophole_usage > 0:
            return True
        return False

    def use_loophole(self):
        """
        抜け穴の使用時の処理
        """
        pos = (self.position[0], self.position[1])
        if self.loophole_usage > 0 and pos in self.loopholes:
            print(f"\n{Color.RED}<<<抜け穴を使用しました！！！！！！！！！！！！>>>{Color.RESET}")
            self.loophole_usage -= 1
            print(f"残り抜け穴使用回数：{self.loophole_usage}\n")
            selected_exit = random.choice(self.loopholes[pos])
            self.position = list(selected_exit)
            new_item_position = [pos[0], pos[1] + 1] if pos[1] == 0 else [pos[0], pos[1] - 1]
            self.item.add_item(new_item_position)

    def update_vision_board(self):
        """
        視界範囲を更新
        """
        self.vision_board = self.create_vision_board()

    def is_cat_in_vision(self, cat_position):
        """
        視界内に猫がいるかを確認
        """
        mouse_x, mouse_y = self.position
        cat_x, cat_y = cat_position
        return abs(mouse_x - cat_x) <= self.vision_range and abs(mouse_y - cat_y) <= self.vision_range

    def move_towards_destination(self):
        """
        目的地（抜け穴など）に向けて移動
        """
        dx = self.destination[0] - self.position[0]
        dy = self.destination[1] - self.position[1]

        if abs(dx) > abs(dy):
            self.position[0] += 1 if dx > 0 else -1
        elif abs(dy) >= abs(dx):
            self.position[1] += 1 if dy > 0 else -1
    
    def calculate_move_scores(self, cat_position):
        """
        移動候補のスコアを計算（猫との距離）
        """
        scores = {}
        x, y = self.position

        # 上下左右の移動候補を生成
        possible_moves = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if self.is_within_bounds(x + dx, y + dy)  # 移動範囲内か確認
        ]

        # 各移動候補に対してスコアを計算（猫から遠ざかる距離をスコアとする）
        for move in possible_moves:
            distance_to_cat = abs(move[0] - cat_position[0]) + abs(move[1] - cat_position[1])
            scores[move] = distance_to_cat

        return scores

    def auto_move(self, cat_position):
        """
        ネズミの自動行動ロジック（視界内外の処理を分岐）
        """
        self.update_vision_board()
        if self.is_cat_in_vision(cat_position):
            self.last_seen_cat_position = cat_position
            # 移動候補のスコアを計算（猫から遠ざかる）
            move_scores = self.calculate_move_scores(cat_position)
            # スコアが最も高い方向に移動
            if move_scores:
                best_move = max(move_scores, key=move_scores.get)
                self.position = list(best_move)
            # 抜け穴が使えるなら使う
            if tuple(self.position) in self.loopholes.keys() and self.loophole_usage > 0:
                self.use_loophole()
        else:
            self.destination = self.find_second_closest_loophole()
            self.move_towards_destination()

    def random_move(self):
        """
        バケツなど、ランダムに移動する場合の処理
        """
        move_options = [
            (self.position[0] + dx, self.position[1] + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if self.is_within_bounds(self.position[0] + dx, self.position[1] + dy)
        ]
        if move_options:
            self.position = list(random.choice(move_options))

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
        self.items = {'L': 0, 'B': 0, 'S': 0}  # 所持しているアイテムリスト
        self.extra_moves = 1
        self.item = Item(cat_items)
        self.mouse = Mouse(self.item)
        
    def next_move(self, direction, mouse_position, item_position): # ネコの移動先決定
        input_flag = True
        x, y = self.position
        direction_map = {"Q":(-1, -1), "W":(-1, 0), "E":(-1,1),
                         "A":(0,-1), "D":(0,1),
                         "Z":(1,-1), "X":(1,0), "C":(1,1)}
        if direction in direction_map:
            dx, dy = direction_map[direction]
            for hosuu in range(self.extra_moves):
                nx, ny = x + dx, y + dy
                if 0 < nx < BOARD_HEIGHT-1 and 0 < ny < BOARD_WIDTH-1:
                    self.position = [nx, ny]
                    if check_win(self.position, mouse_position):
                        break
                    got_item, i_position = check_get_item(self.position, item_position) 
                    if got_item:
                        item_type = random.choice(self.item.available_items)
                        if item_type == 'L':
                            print(f'{Color.YELLOW}🔶 ライト🔶{Color.RESET} をゲット！')
                        elif item_type == 'S':
                            print(f'{Color.YELLOW}🔶 シューズ🔶{Color.RESET} をゲット！')
                        elif item_type == 'B':
                            print(f"{Color.YELLOW}🔶 バケツ🔶{Color.RESET} をゲット！")
                        self.items[item_type] += 1 
                        self.item.remove_item(i_position, item_position)
                            
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
                            self.next_move(next_cat, mouse_position, item_position)
                    else:
                        self.extra_moves = 1
                        return
            if self.extra_moves == 3:
                self.extra_moves = 1

    def use_item(self, game_board):  # アイテム使用処理
        # アイテム名の対応辞書を用意
        item_names = {
            'L': 'ライト',
            'B': 'バケツ',
            'S': 'シューズ'
        }

        while True:
            # 所持アイテムをフィルタリング
            available_items = {can_use: count for can_use, count in self.items.items() if count > 0}
            if not available_items:
                print("アイテムを所持していません")
                return False, [], False

            # 日本語の表示用アイテム辞書を作成
            translated_items = {
                item_names.get(key, key): f"{value}つ" for key, value in available_items.items()
            }

            print(f"所持アイテム: {translated_items}")
            choice = input("アイテムを使用(1:ライト, 2:バケツ, 3:シューズ), 4:キャンセル>>>")


            try:
                choice = int(choice)
                if choice in [1, 2, 3, 4]:
                    if choice == 4:
                        print("アイテムの使用をキャンセルしました")
                        return False, [], False
                    item_keys = list(self.items.keys())
                    selected_item = item_keys[choice - 1]
                    if self.items[selected_item] > 0:
                        self.items[selected_item] -= 1
                        light_positions = self.item.apply_effect(self.position, selected_item, game_board)
                        if selected_item == "S":
                            self.extra_moves = 3
                            return False, light_positions, False
                        elif selected_item == "B":
                            return True, light_positions, False
                        elif selected_item == "L":
                            return False, light_positions, True
                        break
                    else:
                        print("そのアイテムを持っていない！")
                else:
                    print("無効な入力です。1から4の数字を入力してください。")
            except ValueError:
                print("無効な入力です。1~4の数字のみ入力してください。")
                
                    

class Item:  # アイテム3種の管理
    def __init__(self, cat_items):
        self.items = []
        self.available_items = [item for item in ITEMS if item not in cat_items]
        self.type = random.choice(self.available_items)
    
    def add_item(self, position):
        self.items.append(position)
        
    def remove_item(self, position, items):
        for p in items:
            if p == position:
                items.remove(position)
        
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
    
    
    
class Color: # 文字色定義
	BLACK          = '\033[30m'#(文字)黒
	RED            = '\033[31m'#(文字)赤
	GREEN          = '\033[32m'#(文字)緑
	YELLOW         = '\033[33m'#(文字)黄
	BLUE           = '\033[34m'#(文字)青
	MAGENTA        = '\033[35m'#(文字)マゼンタ
	CYAN           = '\033[36m'#(文字)シアン
	RESET          = '\033[0m'#全てリセット

  

def make_board():
    return [["#" if i == 0 or j == 0 or i == BOARD_HEIGHT-1 or j == BOARD_WIDTH-1 else '.' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

def update_vision_board(game_board, vision_board, cat_position, mouse_position, item, active_player, loopholes, bucket_effect_active, light_effect_positions):
    # item_positions = get_all_item_positions(item)
    if active_player == 'cat':
        vision_range = 1
        vision_center = cat_position
        other_position = mouse_position
        display_other = f'{Color.RED}M{Color.RESET}'
    else:
        if bucket_effect_active:
            vision_range = 0
        else:
            vision_range = 2
        vision_center = mouse_position
        other_position = cat_position
        display_other = f'{Color.GREEN}C{Color.RESET}'
    # 目隠し
    for i in range(1,BOARD_HEIGHT-1):
        for j in range(1,BOARD_WIDTH-1):
            vision_board[i][j] = "X"
    for i in range(BOARD_HEIGHT-1):
        for j in range(BOARD_WIDTH):
            for loophole in loopholes:
                if [i, j] == list(loophole):
                    vision_board[i][j] = f'{Color.BLACK}h{Color.RESET}'
            
    # 通常の視界範囲
    for i in range(max(0, vision_center[0] - vision_range), min(BOARD_HEIGHT, vision_center[0] + vision_range + 1)):
        for j in range(max(0, vision_center[1] - vision_range), min(BOARD_WIDTH, vision_center[1] + vision_range + 1)):
            vision_board[i][j] = game_board[i][j]
            if [i, j] in item:
                vision_board[i][j] = f'{Color.MAGENTA}I{Color.RESET}'
            if [i, j] == other_position:
                vision_board[i][j] = display_other
            for loophole in loopholes:
                if [i, j] == list(loophole):
                    vision_board[i][j] = f'{Color.BLACK}h{Color.RESET}'
                    
    # ライト効果の適用
    for x, y in light_effect_positions:
        if 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH:
            vision_board[x][y] = game_board[x][y]
            if [x, y] == other_position:
                vision_board[x][y] = display_other
            elif [x, y] in item:
                vision_board[x][y] = f'{Color.MAGENTA}I{Color.RESET}'
            for loophole in loopholes:
                if [x, y] == list(loophole):
                    vision_board[x][y] = f'{Color.BLACK}h{Color.RESET}'
    if active_player == 'cat':
        vision_board[vision_center[0]][vision_center[1]] = f"{Color.GREEN}C{Color.RESET}"
    elif active_player == 'mouse':
        vision_board[vision_center[0]][vision_center[1]] = f"{Color.RED}M{Color.RESET}"
    return vision_board

def final_position(cat_position, mouse_position, item_position, loopholes):
    final_board = make_board()
    final_board[cat_position[0]][cat_position[1]] = f'{Color.GREEN}C{Color.RESET}'  # ネコの位置を表示
    final_board[mouse_position[0]][mouse_position[1]] = f'{Color.RED}M{Color.RESET}'# ネズミの位置を表示
    for i_p in item_position:

        final_board[i_p[0]][i_p[1]] = f'{Color.MAGENTA}I{Color.RESET}'  # アイテムの位置を表示
    for loophole in loopholes:
        final_board[loophole[0]][loophole[1]] = f'{Color.BLACK}h{Color.RESET}'  # 抜け穴の位置を表示
    print_board(final_board)

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def check_win(cat_position, mouse_position):
    return cat_position == mouse_position

def check_get_item(cat_position, item_position):
    if cat_position in item_position:
        for i_p in item_position:
            if cat_position == i_p:
                return True, i_p
    return False, None

def game_loop():
    game_board = make_board()  # ゲーム全体の状態を管理するマップ
    vision_board = make_board()  # プレイヤーに表示されるマップ
    cat = Cat()
    item = Item(cat_items)
    mouse = Mouse(item)
    turn_count = 1
    game_over = False  # ゲームの終了を管理するフラグ1
    bucket_effect_active = False # バケツの管理フラグ
    light_effect_positions = []  # ライトの照らしたマスのリスト
    cat_turn = 15-int(turn_count/2)+1
    
    item.add_item([3, 4])

    while turn_count < 31 and not game_over:  # ゲーム終了フラグを確認
        if turn_count % 2 == 1:
            # ネズミのターン
            active_player = 'mouse'            
        else:
            # ネコのターン
            active_player = 'cat'

        # ネコ、ネズミ、アイテムの位置を更新した表示マップを作成
        update_vision_board(game_board, vision_board, cat.position, mouse.position, item.items, active_player, mouse.loopholes, bucket_effect_active, light_effect_positions)
        # print_board(vision_board)

        if turn_count % 2 == 1:
            while True:
                if bucket_effect_active:
                    mouse.random_move()
                    update_vision_board(game_board, vision_board, cat.position, mouse.position, item.items, active_player, mouse.loopholes, bucket_effect_active, light_effect_positions)
                    # print_board(vision_board)
                    bucket_effect_active = False
                else:
                    mouse.auto_move(cat.position)
                    update_vision_board(game_board, vision_board, cat.position, mouse.position, item.items, active_player, mouse.loopholes, bucket_effect_active, light_effect_positions)
                    # print_board(vision_board)
                if check_win(cat.position, mouse.position):
                    print(f"{Color.RED}勝利！ネズミが突っ込んできた！{Color.RESET}")
                    print("  |＼＿／|\n　|―　―  |\n　(o)(o)ノ_＿＿／/\n   \--/         /\n   m\/m |~~~    ヽ\n  mノm_／｣/_／＼｣")
                    game_over = True  # ゲーム終了フラグを設定
                    break
                turn_count += 1
                cat_turn -= 1
                print("~~~~~~~~~~~~~")
                if cat_turn >= 10:
                    print(f"{Color.CYAN}残りのターン{cat_turn}{Color.RESET}\n")
                    break
                elif 4 <= cat_turn <= 9 :
                    print(f"{Color.YELLOW}残りのターン{cat_turn}{Color.RESET}\n")
                    break
                else:
                    print(f"{Color.RED}残りのターン{cat_turn}{Color.RESET}\n")
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
            print_board(vision_board)
            n = 0
            while True:
                if n == 0:
                    cat_move = input("ネコの移動 (QWEADZXC) | アイテム使用 (I) : ").upper()
                    if cat_move == "I":
                        bucket_effect_active, l_positions, light_effect = cat.use_item(game_board)
                        for positions in l_positions:
                            light_effect_positions.append(positions)
                        if light_effect:
                            update_vision_board(game_board, vision_board, cat.position, mouse.position, item.items, active_player, mouse.loopholes, bucket_effect_active, light_effect_positions)
                            print_board(vision_board)
                        n += 1
                    elif cat_move in ["Q","W","E","A","D","Z","X","C"]:
                        cat.next_move(cat_move, mouse.position, item.items)
                        if check_win(cat.position, mouse.position):
                            print(f"{Color.RED}✨✨ 勝利！ネズミをつかまえた！✨✨{Color.RESET}")
                            print("  |＼＿／|\n　|―　―  |\n　(o)(o)ノ_＿＿／/\n   \--/         /\n   m\/m |~~~    ヽ\n  mノm_／｣/_／＼｣")
                            game_over = True  # ゲーム終了フラグを設定
                        turn_count += 1
                        break
                    else:
                        print("入力が間違っている！！")
                else:
                    cat_move = input("ネコの移動 (QWEADZXC) : ").upper()
                    if cat_move in ["Q","W","E","A","D","Z","X","C"]:
                        cat.next_move(cat_move, mouse.position, item.items)
                        if check_win(cat.position, mouse.position):
                            print(f"{Color.RED}✨✨ 勝利！ネズミをつかまえた！✨✨{Color.RESET}")
                            print("  |＼＿／|\n　|―　―  |\n　(o)(o)ノ_＿＿／/\n   \--/         /\n   m\/m |~~~    ヽ\n  mノm_／｣/_／＼｣")
                            game_over = True  # ゲーム終了フラグを設定
                        turn_count += 1
                        break
                    else:
                        print("入力が間違っていませんか？")
    
    if not game_over:
        print(f"{Color.BLUE}ネズミに逃げられてしまった...{Color.RESET}")  # ターン数に到達してもゲームが終了しない場合
        print(f"⠀　　　{Color.YELLOW}+ ⊂⊃{Color.RESET}\n　 　　　∧_∧　{Color.YELLOW}+{Color.RESET}\n　　　　( ᴗ ̫ᴗ)\n　　　i⌒/ つつ          ε=ε=ε= ～(⌒C・>")
        final_position(cat.position, mouse.position, item.items, mouse.loopholes)

def print_rule():
        print("\n  |\      _,,,---,,_                  _  _")
        print("  /,`.-'`'    -.  ;-;;,_             (o)(o)--.")
        print(" |,4-  ) )-,_..;\ (  `'-'   VS        \../ (  )hjw")
        print("'---''(_/--'  `-'\_)                  m\/m--m'`--.")
        print("\nLet's play C A T & M O U S E\n")

        print("=== ルール ===")
        # ターンについて
        print(f"{Color.YELLOW}～ ターンについて ～{Color.RESET}")
        print("15ターン以内にネズミを捕まえたらネコの勝利です！")
        print("1ターンに1マス移動が必要です。")
        print("")
        # 移動方法について
        print(f"{Color.YELLOW}～ 移動方法について ～{Color.RESET}")
        print("ネコの移動キー:\n↖q ↑w e↗\n←a s d→\n↙z ↓x c↘")
        print("ネズミの移動範囲は上下左右の4方向です。")
        print("")
        # ネズミについて
        print(f"{Color.YELLOW}～ネズミについて～{Color.RESET}")
        print(f"ネズミが抜け穴(マップ上の「{Color.BLACK}h{Color.RESET}」)を使用すると他のランダムな抜け穴から出てきます。")
        print("ネズミが抜け穴を使用できるのは2回までです。")
        print("")
        # アイテムの仕様について
        print(f"{Color.YELLOW}～ アイテム ～{Color.RESET}")
        print(f"アイテムは、ライト,シューズ,バケツ の三種類。\nゲーム開始時に部屋のどこかに1つ落ちている他、\nネズミが抜け穴を使用するとランダムで1つ、使用された抜け穴の位置に「{Color.MAGENTA}I{Color.RESET}」として生成されます。\n")
        print(f"{Color.YELLOW}～アイテムの使用方法について～{Color.RESET}\n数字キーにて  1=ライト、2=バケツ、3=シューズ\nを所持しているアイテムに応じて押してください。\nアイテム使用をキャンセルしたい場合は、数字キー 4 を押してください。")
        # アイテムの説明
        print("")
        print(f"{Color.YELLOW}～アイテムの効果～{Color.RESET}")
        print("ライト：方向を指定して、壁までマスを明るく照らします！")
        print("バケツ：次のネズミのターン時、視界を0にします。さらに、ネズミの移動先を上下左右のランダムにします。")
        print("シューズ：移動時に＋２マス進めます！")
        print("")
        # 視界範囲について
        print(f"{Color.YELLOW}～ 視界範囲について ～{Color.RESET}")
        print(f"ネコの視界:\n      〇 〇 〇\n      〇 {Color.GREEN}Ｃ{Color.RESET} 〇\n      〇 〇 〇\n      {Color.GREEN}Ｃ{Color.RESET}をネコとすると〇が見える範囲となります。")
        print("")
        print(f"ネズミの視界:\n      〇 〇 〇 〇 〇\n      〇 〇 〇 〇 〇\n      〇 〇 {Color.RED}Ｍ{Color.RESET} 〇 〇\n      〇 〇 〇 〇 〇\n      〇 〇 〇 〇 〇\n      {Color.RED}Ｍ{Color.RESET}をネズミとすると〇が見える範囲となります。")
        print("")
        # ゲーム開始
        input("ネズミを捕まえる準備はできましたか？(Enter)>>>")



if __name__ == "__main__":  #起動
    print_rule()
    game_loop()