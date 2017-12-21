/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50711
Source Host           : 127.0.0.1:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2017-08-31 14:43:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for video_download
-- ----------------------------
DROP TABLE IF EXISTS `video_download`;
CREATE TABLE `video_download` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '该表用来下载视频并合并',
  `download_url` varchar(255) NOT NULL,
  `init_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `start_down_time` datetime DEFAULT NULL,
  `downloaded_time` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0' COMMENT '0:将被下载;1:下载完成;2:下载失败',
  `video_path` varchar(255) DEFAULT NULL,
  `sub_title_path` varchar(255) DEFAULT NULL,
  `merge_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
