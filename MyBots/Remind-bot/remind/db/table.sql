-- ----------------------------
-- Table structure for bot_users
-- ----------------------------
CREATE TABLE if not exists `bot_users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL default '' COMMENT '用户ID',
  `user_name` varchar(30) NOT NULL default '' COMMENT '用户名',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为管理员',
  `start_time` int(11) DEFAULT NULL COMMENT '开始使用时间',
  `group_id` varchar(10) NOT NULL default '' COMMENT '所属组ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for bot_links
-- ----------------------------
CREATE TABLE if not exists `bot_links` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL COMMENT '用户ID',
  `link` varchar(255) DEFAULT NULL COMMENT '订阅链接',
  `delete_time` int(11) DEFAULT NULL COMMENT '删除时间',
  `update_time` int(11) DEFAULT NULL COMMENT '更新时间',
  `create_time` int(11) DEFAULT NULL COMMENT '添加时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for bot_links
-- ----------------------------
CREATE TABLE if not exists `groups` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `group_id` varchar(10) DEFAULT NULL COMMENT '组ID',
  `user_id` varchar(10) NOT NULL COMMENT '用户ID',
  `group_name` varchar(255) NOT NULL COMMENT '组名',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为管理员',
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for spider_data
-- ----------------------------
CREATE TABLE if not exists `spider_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL default '' COMMENT '标题',
  `last_episode` varchar(255) NOT NULL default '' COMMENT '最新集',
  `last_episode_title` varchar(255) NOT NULL default '' COMMENT '最新集标题',
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for batch_spider_integration_task
-- ----------------------------
CREATE TABLE `batch_spider_integration_task` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `subscribe_number` int(8) NOT NULL DEFAULT '1' COMMENT '订阅人数',
  `link` varchar(255) DEFAULT NULL COMMENT '抓取链接',
  `parser_name` varchar(255) DEFAULT NULL,
  `state` int(11) DEFAULT '0' COMMENT '抓取状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `link` (`link`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of batch_spider_task
-- ----------------------------