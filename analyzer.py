import cv2 as cv
import numpy as np

from obj_analyzer.segmentation import ResUnet
import obj_analyzer.keypoints as kp
import utils.image as iu


class Analyzer:
    def perspective_transform(self, img_src, img_dst, corners):
        pts_src = np.array([[0, 0], [255, 0], [255, 255], [0, 255]])
        pts_dst = np.array(corners)
        h, status = cv.findHomography(pts_src, pts_dst)
        img_out = cv.warpPerspective(img_src, h, (img_dst.shape[1], img_dst.shape[0]))
        return img_out

    def image_work(self, img1, img2, mask1, mask2):
        img1 = iu.convert_to_gray(img1)
        img2 = iu.convert_to_gray(img2)
        key_points_img, corners = kp.draw_key_points(img1, img2)
        cv.imshow('kp', key_points_img)

        perspective = self.perspective_transform(img1, key_points_img, corners)
        mask_corners = corners.copy()
        mask_corners[:, 0] -= 255
        perspective_mask = self.perspective_transform(mask1, mask2, mask_corners)

        return perspective, perspective_mask

    def analyze(self, images):
        sgm = ResUnet()
        sgm.get_model()

        images = [iu.resize(img, (256, 256)) for img in images]
        # img1 = iu.resize(img1, (256, 256))
        # img2 = iu.resize(img2, (256, 256))

        masks = [sgm.predict(img) for img in images]
        for i, mask in enumerate(masks):
            cv.imshow(f"mask{i}", mask)

        # mask1 = sgm.predict(img1)
        # mask2 = sgm.predict(img2)

        # cv.imshow('mask1', mask1)
        # cv.imshow('mask2', mask2)

        for i, (img, mask) in enumerate(zip(images, masks)):
            if i == (len(images) - 1):
                break
            transform, transform_mask = self.image_work(img, images[i + 1], mask, masks[i + 1])
            cv.imshow(f"transform{i}->{i+1}", transform)
            cv.imshow(f"transform_mask{i}->{i+1}", transform_mask)
            area1 = iu.get_mask_area(transform_mask)
            area2 = iu.get_mask_area(masks[i+1])
            print(f"area transform {i} -> {i+1}: {area2 / area1}")

        # transform, transform_mask = self.image_work(img1, img2, mask1, mask2)
        # cv.imshow('transform', transform)
        # cv.imshow('transform_mask', transform_mask)
        #
        # area1 = iu.get_mask_area(transform_mask)
        # area2 = iu.get_mask_area(mask2)
        #
        # print(area2 / area1)
        #
        # img1 = iu.add_mask(img1, mask1)
        # img2 = iu.add_mask(img2, mask2)
        # #
        # cv.imshow('s1', img1)
        # cv.imshow('s2', img2)

        cv.waitKey()