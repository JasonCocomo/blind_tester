DROP TABLE `file`;
CREATE TABLE `file` (
  `file_id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '文件id',
  `filename` VARCHAR(128) NOT NULL COMMENT '文件名',
  `file_type` VARCHAR(16) NOT NULL COMMENT '文件类型, face:人脸，material: 素材',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`file_id`),
  UNIQUE KEY (`filename`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人脸表';
DROP TABLE `face`;
CREATE TABLE `face` (
  `face_id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '人脸id',
  `file_id` BIGINT NOT NULL COMMENT '文件id',
  `filename` VARCHAR(128) NOT NULL COMMENT '文件名',
  `skin_color` BIGINT NOT NULL COMMENT '国家',
  `age_range` BIGINT NOT NULL COMMENT '年龄范围,0: 五岁以下，1：16岁以下，3:40岁以下，4：大于40',
  `gender` INT NOT NULL COMMENT '0:女，1：男',
  `roughness` INT NOT NULL COMMENT '面部粗糙程度，0:光滑，1：较为光滑，2：一般，3：较粗糙，4：粗糙',
  `remark` VARCHAR(256) NOT NULL COMMENT '人脸描述，可用于检索',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`face_id`),
  KEY (`skin_color`, `age_range`, `gender`, `roughness`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人脸表';
DROP TABLE `face_group`;
CREATE TABLE `face_group` (
  `fg_id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '人脸组id',
  `name` VARCHAR(64) NOT NULL COMMENT "人脸组名称",
  `remark` VARCHAR(256) NOT NULL COMMENT "备注",
  `status` INT NOT NULL DEFAULT '0' COMMENT '人脸组状态，0：可以增删人脸，1：不可更改',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`fg_id`),
  UNIQUE KEY (`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人脸组表，集中管理人脸';
DROP TABLE `joined_face_group`;
CREATE TABLE `joined_face_group` (
  `fg_id` BIGINT NOT NULL COMMENT '人脸组id',
  `face_id` BIGINT NOT NULL COMMENT '人脸id',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`fg_id`, `face_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人脸数据集';
DROP TABLE `swap_pair`;
CREATE TABLE `swap_pair` (
  `sp_id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '换脸对id',
  `face_id` BIGINT NOT NULL COMMENT '人脸ID',
  `material_id` BIGINT NOT NULL COMMENT '素材id',
  `remark` VARCHAR(256) NOT NULL COMMENT "备注",
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`sp_id`),
  UNIQUE KEY (`material_id`, `face_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '换脸对';
DROP TABLE `swap_pair_dataset`;
CREATE TABLE `swap_pair_dataset` (
  `spd_id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '换脸对数据集id',
  `name` VARCHAR(64) NOT NULL COMMENT '换脸对数据集名称',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`spd_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '换脸对数据集';
DROP TABLE `swap_pair_group`;
CREATE TABLE `swap_pair_group` (
  `spd_id` BIGINT NOT NULL COMMENT '换脸对数据集id',
  `sp_id` BIGINT NOT NULL COMMENT '换脸对id',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`spd_id`, `sp_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '换脸对数组';