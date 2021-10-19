
DROP TABLE `dataset`;
CREATE TABLE `dataset` (
  `id` BIGINT AUTO_INCREMENT COMMENT '数据集id',
  `name` VARCHAR(128) NOT NULL COMMENT '数据集名',
  `data_dir` VARCHAR(256) NOT NULL COMMENT '数据集所在目录',
  `remark` VARCHAR(1024) DEFAULT NULL COMMENT '备注',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '测试数据集表';
DROP TABLE `material`;
CREATE TABLE `material` (
  `material_id` BIGINT AUTO_INCREMENT COMMENT '素材id',
  `basename` VARCHAR(64) NOT NULL COMMENT '文件basename',
  `mtype` VARCHAR(16) NOT NULL COMMENT '素材类型，video,gif,image',
  `dataset_id` BIGINT NOT NULL COMMENT '归属数据集id',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`material_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '测试数据集表';
DROP TABLE `swap_test`;
CREATE TABLE `swap_test` (
  `swap_id` BIGINT AUTO_INCREMENT COMMENT '换脸测试id',
  `name` VARCHAR(256) NOT NULL COMMENT '测试名',
  `result_dir` VARCHAR(256) NOT NULL COMMENT '换脸结果目录',
  `dataset_id` BIGINT NOT NULL COMMENT "数据集id",
  `remark` VARCHAR(1024) DEFAULT NULL COMMENT '备注',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`swap_id`),
  KEY `name_index` (`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '换脸测试表';
DROP TABLE `comparation_group`;
CREATE TABLE `comparation_group` (
  `cg_id` BIGINT AUTO_INCREMENT COMMENT '比对组id',
  `src_id` BIGINT NOT NULL COMMENT '源换脸测试id',
  `target_id` BIGINT NOT NULL COMMENT '目标换脸测试id',
  `dataset_id` BIGINT NOT NULL COMMENT '数据集id',
  `remark` VARCHAR(1024) DEFAULT NULL COMMENT '备注',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`cg_id`),
  UNIQUE KEY (`src_id`, `target_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '评测比对组表';
DROP TABLE `comparation_result`;
CREATE TABLE `comparation_result` (
  `cr_id` BIGINT AUTO_INCREMENT COMMENT '比对结果id',
  `cg_id` BIGINT NOT NULL COMMENT '比对组id',
  `c_order` VARCHAR(2048) NOT NULL COMMENT '随机顺序',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`cr_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '评测比对结果表';

DROP TABLE comparation_result_score;
CREATE TABLE `comparation_result_score` (
  `crs_id` BIGINT AUTO_INCREMENT COMMENT '比对结果得分id',
  `cr_id` BIGINT NOT NULL COMMENT '比对结果id',
  `cg_id` BIGINT NOT NULL COMMENT '比对组id',
  `target_score` VARCHAR(2048) NOT NULL COMMENT '目标得分',
  `score_dim` VARCHAR(32) NOT NULL COMMENT '打分维度',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`crs_id`),
  KEY (`cr_id`, `score_dim`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '评测比对结果表';