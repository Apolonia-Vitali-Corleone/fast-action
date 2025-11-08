-- MySQL初始化脚本
-- 数据库：course_system

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `course_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `course_system`;

-- 删除旧表（如果存在）
DROP TABLE IF EXISTS `enrollments`;
DROP TABLE IF EXISTS `courses`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `teachers`;
DROP TABLE IF EXISTS `django_session`;
DROP TABLE IF EXISTS `django_admin_log`;
DROP TABLE IF EXISTS `django_content_type`;
DROP TABLE IF EXISTS `auth_permission`;
DROP TABLE IF EXISTS `auth_group_permissions`;
DROP TABLE IF EXISTS `auth_group`;

-- Django系统表
CREATE TABLE `django_session` (
  `session_key` VARCHAR(40) NOT NULL PRIMARY KEY,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME(6) NOT NULL,
  INDEX `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `django_content_type` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `auth_permission` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `content_type_id` INT NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `auth_group` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `auth_group_permissions` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `group_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `django_admin_log` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `action_time` DATETIME(6) NOT NULL,
  `object_id` LONGTEXT,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT UNSIGNED NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT,
  `user_id` INT,
  INDEX `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  INDEX `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Django migrations表
CREATE TABLE `django_migrations` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 学生表
CREATE TABLE `students` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `email` VARCHAR(255) NOT NULL UNIQUE COMMENT '邮箱',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生表';

-- 教师表
CREATE TABLE `teachers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `email` VARCHAR(255) NOT NULL UNIQUE COMMENT '邮箱',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教师表';

-- 课程表
CREATE TABLE `courses` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(200) NOT NULL COMMENT '课程名称',
  `description` TEXT COMMENT '课程描述',
  `teacher_id` INT NOT NULL COMMENT '教师ID（应用层关联）',
  `capacity` INT NOT NULL DEFAULT 50 COMMENT '容量',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_teacher_id` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 选课记录表
CREATE TABLE `enrollments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL COMMENT '学生ID（应用层关联）',
  `course_id` INT NOT NULL COMMENT '课程ID（应用层关联）',
  `enrolled_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '选课时间',
  INDEX `idx_student_course` (`student_id`, `course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='选课记录表';

-- 插入测试数据（密码都是: password123，已经用Django的make_password加密）
-- 测试学生
INSERT INTO `students` (`username`, `password`, `email`) VALUES
('student1', 'pbkdf2_sha256$600000$yuxKmTcx5gEpqYHS8SzVUV$b2Pj8DkJj0yVYhvA2EGPrzRhVApLfTyeXqeZ7A9gWo0=', 'student1@test.com'),
('student2', 'pbkdf2_sha256$600000$aU0rTWrwRQYeY1K5ZNyeWc$cUKFdUunu7w317d0otqiiA/FD1s+GdGosHBhYy+jSjY=', 'student2@test.com');

-- 测试教师
INSERT INTO `teachers` (`username`, `password`, `email`) VALUES
('teacher1', 'pbkdf2_sha256$600000$yBWYx2XU7Fe77F5blN0ptT$6kZId4KCrTgRgDYGzUMnnrsO6pxrGPf+heinHXrlsoA=', 'teacher1@test.com'),
('teacher2', 'pbkdf2_sha256$600000$3DvDze07fSuTR0mYC66SEl$z7GkjWsZd31NQ3OZ3Ju1V0CVBCLHzXnKUcuyu6jiR+E=', 'teacher2@test.com');

-- 测试课程
INSERT INTO `courses` (`name`, `description`, `teacher_id`, `capacity`) VALUES
('Python编程', 'Python基础到进阶', 1, 30),
('Web开发', 'Django框架实战', 1, 40),
('数据库设计', 'MySQL从入门到精通', 2, 25);

-- 测试选课记录
INSERT INTO `enrollments` (`student_id`, `course_id`) VALUES
(1, 1),
(1, 2),
(2, 1);
