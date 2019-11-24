
import numpy as np
import pygame

# TODO: commit to github


class Run(object):
    def __init__(self):
        self.map_size = (500, 500)
        self._is_open_mat = None

        self.batman = {
            'location': {'row': 50, 'col': 50},  # starting location
            'size': {'width': 40, 'height': 60},
            'speed': 20,
        }

    @property
    def is_open_mat(self):
        if self._is_open_mat is None:
            is_open_mat = np.ones(self.map_size, dtype=bool)
            is_open_mat[0, :] = False
            is_open_mat[-1, :] = False
            is_open_mat[:, 0] = False
            is_open_mat[:, -1] = False
            is_open_mat[:300, 400] = False
            is_open_mat[380:, 400] = False
            is_open_mat[300, :100] = False
            is_open_mat[300, 250:400] = False
            self._is_open_mat = is_open_mat

        return self._is_open_mat

    def run(self):
        pygame.init()

        win = pygame.display.set_mode(self.map_size)
        pygame.display.set_caption("Batman Game")

        run = True
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            self._update_character_longitude(
                character_name='batman', keys=keys)
            self._update_character_latitude(
                character_name='batman', keys=keys)

            self._draw_background(window=win)
            self._draw_batman(window=win)

            pygame.display.update()

        pygame.quit()

    def _update_character_longitude(self, character_name, keys):
        if character_name == 'batman':
            row = self.batman['location']['row']
            col = self.batman['location']['col']
            width = self.batman['size']['width']
            height = self.batman['size']['height']
            speed = self.batman['speed']
        else:
            raise ValueError('unsupported character {}'.format(character_name))

        start_position_x = row

        if keys[pygame.K_LEFT]:
            row -= speed
        if keys[pygame.K_RIGHT]:
            row += speed

        if row < 0:
            row = 0
        elif row > self.map_size[1]:
            row = self.map_size[1]

        if row > start_position_x:  # moved right
            mat_x = self.is_open_mat[
                col:(col + height),
                (start_position_x + width):(row + width)]
            mat_x = ~((~mat_x).sum(axis=0) > 0)
            row = int(
                start_position_x +
                np.where(~np.append(mat_x, False))[0][0].squeeze())
        elif row < start_position_x:  # moved left
            mat_x = self.is_open_mat[
                col:(col + height), row:start_position_x]
            mat_x = ~((~mat_x).sum(axis=0) > 0)
            row = int(start_position_x - (
                len(mat_x) -
                np.where(~np.append(False, mat_x))[0][-1].squeeze()))

        self.batman['location']['row'] = row

    def _update_character_latitude(self, character_name, keys):
        if character_name == 'batman':
            row = self.batman['location']['row']
            col = self.batman['location']['col']
            width = self.batman['size']['width']
            height = self.batman['size']['height']
            speed = self.batman['speed']
        else:
            raise ValueError('unsupported character {}'.format(character_name))

        start_position_y = col

        if keys[pygame.K_UP]:
            col -= speed
        if keys[pygame.K_DOWN]:
            col += speed

        if col < 0:
            col = 0
        elif col > self.map_size[0]:
            col = self.map_size[0]

        if col < start_position_y:  # moved up
            mat_y = self.is_open_mat[
                col:start_position_y, row:(row + width)]
            mat_y = ~((~mat_y).sum(axis=1) > 0)
            col = int(start_position_y - (
                len(mat_y) -
                np.where(~np.append(False, mat_y))[0][-1].squeeze()))
        elif col > start_position_y:  # moved down
            mat_y = self.is_open_mat[
                (start_position_y + height):(col + height),
                row:(row + width)]
            mat_y = ~((~mat_y).sum(axis=1) > 0)
            col = int(
                start_position_y +
                np.where(~np.append(mat_y, False))[0][0].squeeze())

        self.batman['location']['col'] = col

    def _draw_background(self, window):
        window.fill((255, 255, 255))
        for i in range(self.is_open_mat.shape[0]):
            for j in range(self.is_open_mat.shape[1]):
                if not self.is_open_mat[i, j]:
                    pygame.draw.rect(window, (0, 0, 0), (j, i, 1, 1))

    def _draw_batman(self, window):
        pygame.draw.rect(window, (0, 0, 0),
                         (self.batman['location']['row'],
                          self.batman['location']['col'],
                          self.batman['size']['width'],
                          self.batman['size']['height']))


if __name__ == '__main__':
    r = Run()
    r.run()
