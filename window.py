import pygame
pygame.init()

# Window
WIN_LENGTH = 1200
WIN_WIDTH = 725
WIN_TITLE = "Inorder, Preorder, Postorder Traversal Visualizer"

# Colors
WHITE = (255, 255, 255)
EGG_WHITE = (239, 235, 221)
SPRING_GREEN = (0, 240, 168)
BLACK = (0, 0, 0)
BONE_WHITE = (249, 246, 238)
DARK = (50, 50, 50)
INDIGO = (31, 81, 255)

# Font
GEORGIA = pygame.font.SysFont('georgia', 30)

# Button Dimensions and Labels
BUTTON_X = 90
BUTTON_Y = 70
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_SPACING = 360

INORDER_LABEL = "Inorder Traversal"
PREORDER_LABEL = "Preorder Traversal"
POSTORDER_LABEL = "Postorder Traversal"

# Node Dimensions
NODE_RADIUS = 40
NODE_GAP = 100
SPECIAL_NODE_1 = 3
SPECIAL_NODE_2 = 10
SPECIAL_NODE_3 = 8


class Button:

    def __init__(self, color, x, y, width, height, label=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

    def draw_border(self, win):
        # see if line below can be improved
        outer_box = (self.x - 3, self.y - 3,
                     self.width + 6, self.height + 6)
        pygame.draw.rect(win, DARK, outer_box, 0)

    def draw_label(self, win):
        text = GEORGIA.render(self.label, True, BLACK)
        # see if lines below can be improved
        text_x = self.x + (self.width/2 - text.get_width()/2)
        text_y = self.y + (self.height/2 - text.get_height()/2)
        win.blit(text, (text_x, text_y))

    def draw_button(self, win):
        self.draw_border(win)
        inner_box = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, inner_box, 0)
        self.draw_label(win)

    def has_mouse(self, mouse_position):
        within_x = self.x < mouse_position[0] < self.x + self.width
        within_y = self.y < mouse_position[1] < self.y + self.height
        if within_x and within_y:
            return True
        return False


class Node:

    def __init__(self, color, x, y, radius, value):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value
        self.left = None
        self.right = None

    def draw_value(self, win):
        value = GEORGIA.render(str(self.value), True, BLACK)
        value_x = self.x - value.get_width()/2
        value_y = self.y - value.get_height()/2
        win.blit(value, (value_x, value_y))

    def draw_border(self, win,):
        border_radius = self.radius + 3
        pygame.draw.circle(win, DARK, (self.x, self.y), border_radius)

    def draw_node(self, win):
        self.draw_border(win)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        self.draw_value(win)

    def create_new_left(self, new_val):
        new_x = self.x - NODE_GAP
        new_y = self.y + NODE_GAP
        self.left = Node(EGG_WHITE, new_x, new_y, NODE_RADIUS, new_val)
        if self.left.value is SPECIAL_NODE_1:
            self.left.x -= NODE_GAP

    def create_new_right(self, new_val):
        new_x = self.x + NODE_GAP
        new_y = self.y + NODE_GAP
        self.right = Node(EGG_WHITE, new_x, new_y, NODE_RADIUS, new_val)
        if self.right.value == SPECIAL_NODE_2:
            self.right.x += NODE_GAP

    def insert(self, new_val):
        if new_val < self.value:
            if self.left is None:
                self.create_new_left(new_val)
            else:
                self.left.insert(new_val)
        else:
            if self.right is None:
                self.create_new_right(new_val)
            else:
                self.right.insert(new_val)
        return self

    def light_up_node(self, win):
        self.color = INDIGO
        self.draw_node(win)
        pygame.display.update()

        pygame.time.delay(500)

        self.color = EGG_WHITE
        self.draw_node(win)
        pygame.display.update()

    def draw_all_nodes(self, node, win):
        if node is not None:
            self.draw_all_nodes(node.left, win)
            node.draw_node(win)
            self.draw_all_nodes(node.right, win)

    def inorder_traversal(self, node, win):
        if node is not None:
            self.inorder_traversal(node.left, win)
            node.light_up_node(win)
            self.inorder_traversal(node.right, win)

    def preorder_traversal(self, node, win):
        if node is not None:
            node.light_up_node(win)
            self.preorder_traversal(node.left, win)
            self.preorder_traversal(node.right, win)

    def postorder_traversal(self, node, win):
        if node is not None:
            self.postorder_traversal(node.left, win)
            self.postorder_traversal(node.right, win)
            node.light_up_node(win)

    def calculate_node_gap(self):
        gap = NODE_GAP
        if self.value == SPECIAL_NODE_3:
            gap = NODE_GAP * 2
        return gap

    def draw_branch(self, node, win):
        start = (self.x, self.y)
        node_gap = self.calculate_node_gap()

        if node.left is not None:
            left_end = (node.x - node_gap, node.y + NODE_GAP)
            pygame.draw.line(win, BLACK, start, left_end, 13)
        if node.right is not None:
            right_end = (node.x + node_gap, node.y + NODE_GAP)
            pygame.draw.line(win, BLACK, start, right_end, 13)

    def draw_all_branches(self, node, win):
        if node is not None:
            self.draw_all_branches(node.left, win)
            node.draw_branch(node, win)
            self.draw_all_branches(node.right, win)


def create_window():
    win = pygame.display.set_mode((WIN_LENGTH, WIN_WIDTH))
    win.fill(BONE_WHITE)
    pygame.display.set_caption(WIN_TITLE)
    return win


def create_button(label, spacing_factor):
    button_x = BUTTON_X + (spacing_factor * BUTTON_SPACING)
    new_button = Button(EGG_WHITE, button_x,
                        BUTTON_Y, BUTTON_WIDTH,
                        BUTTON_HEIGHT, label)
    return new_button


def create_node(x, y, value):
    new_node = Node(EGG_WHITE, x, y, NODE_RADIUS, value)
    return new_node


def set_button_color(button, mouse_position):
    if button.has_mouse(mouse_position):
        button.color = INDIGO
    else:
        button.color = EGG_WHITE


def main():
    win = create_window()

    inorder_button = create_button(INORDER_LABEL, 0)
    preorder_button = create_button(PREORDER_LABEL, 1)
    postorder_button = create_button(POSTORDER_LABEL, 2)

    nodes = [3, 10, 1, 6, 14, 4, 7, 13, 29, 5, -2]

    eight = create_node(600, 215, 8)
    for node in nodes:
        eight.insert(node)

    # loop to keep window running
    run = True
    while run:
        inorder_button.draw_button(win)
        preorder_button.draw_button(win)
        postorder_button.draw_button(win)

        eight.draw_all_branches(eight, win)
        eight.draw_all_nodes(eight, win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                set_button_color(inorder_button, mouse_position)
                set_button_color(preorder_button, mouse_position)
                set_button_color(postorder_button, mouse_position)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if inorder_button.has_mouse(mouse_position):
                    eight.inorder_traversal(eight, win)
                if preorder_button.has_mouse(mouse_position):
                    eight.preorder_traversal(eight, win)
                if postorder_button.has_mouse(mouse_position):
                    eight.postorder_traversal(eight, win)

        pygame.display.update()


main()
