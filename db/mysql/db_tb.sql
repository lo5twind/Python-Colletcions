use test;
/*
Navicat MySQL Data Transfer

Source Server         : test 
Source Server Version : 50630
Source Host           : localhost:3307
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50630
File Encoding         : 65001

Date: 2016-07-12 15:30:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for m_IPS_template_rules
-- ----------------------------
DROP TABLE IF EXISTS `m_IPS_template_rules`;
CREATE TABLE `m_IPS_template_rules` (
  `id` int(11) NOT NULL,
  `iSID` int(11) NOT NULL,
  `sRules` text,
  PRIMARY KEY (`iSID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for m_tbauthenticate_log
-- ----------------------------
DROP TABLE IF EXISTS `m_tbauthenticate_log`;
CREATE TABLE `m_tbauthenticate_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT ,
  `iTime` int(32) DEFAULT NULL ,
  `sUserName` varchar(32) DEFAULT NULL ,
  `sIP` varchar(32) DEFAULT NULL ,
  `iAction` tinyint(1) DEFAULT NULL ,
  `iStatus` tinyint(1) DEFAULT '0' ,
  `iType` tinyint(1) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tbcustom_ips_lib
-- ----------------------------
DROP TABLE IF EXISTS `m_tbcustom_ips_lib`;
CREATE TABLE `m_tbcustom_ips_lib` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sRuleID` varchar(128) DEFAULT NULL ,
  `sRuleName` varchar(128) DEFAULT NULL ,
  `sDesc` varchar(256) DEFAULT NULL ,
  `sRuleType` varchar(256) DEFAULT NULL ,
  `sDangerLever` varchar(64) DEFAULT NULL ,
  `sCharacterString` varchar(512) DEFAULT NULL ,
  `iChartCaseSensitive` tinyint(1) DEFAULT NULL ,
  `sRegularExpressions` varchar(128) DEFAULT NULL ,
  `iRegularCaseSensitive` tinyint(1) DEFAULT NULL ,
  `sProtocol` varchar(64) DEFAULT NULL ,
  `iStatus` tinyint(2) DEFAULT '0' ,
  `iCustomOrInset` tinyint(2) DEFAULT NULL ,
  `sAction` varchar(50) DEFAULT NULL ,
  `sRule` text,
  `sRuleBelongFile` varchar(200) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `i_sRuleID` (`sRuleID`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tbfileset
-- ----------------------------
DROP TABLE IF EXISTS `m_tbfileset`;
CREATE TABLE `m_tbfileset` (
  `sDir` varchar(100) DEFAULT NULL,
  `sDate` varchar(50) DEFAULT NULL,
  `sTime` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for m_tbhoneypot_log
-- ----------------------------
DROP TABLE IF EXISTS `m_tbhoneypot_log`;
CREATE TABLE `m_tbhoneypot_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) DEFAULT NULL ,
  `sProtocol` varchar(128) DEFAULT NULL ,
  `sSourceAddr` varchar(64) DEFAULT NULL ,
  `sSourcePort` varchar(64) DEFAULT NULL ,
  `sTargetAddr` varchar(64) DEFAULT NULL ,
  `sTargetPort` varchar(64) DEFAULT NULL ,
  `iConnectTime` int(11) DEFAULT NULL ,
  `sUserName` varchar(128) DEFAULT NULL ,
  `iCommandTotal` int(11) DEFAULT NULL ,
  `sThreatEvaluate` varchar(256) DEFAULT NULL ,
  `sDetail` varchar(512) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tbhoneypot_status
-- ----------------------------
DROP TABLE IF EXISTS `m_tbhoneypot_status`;
CREATE TABLE `m_tbhoneypot_status` (
  `iId` int(11) NOT NULL,
  `iConnectRootid` int(11) DEFAULT NULL,
  `iConnectParentid` int(11) DEFAULT NULL,
  `sName` varchar(255) DEFAULT NULL ,
  `sConfigName` varchar(255) DEFAULT NULL ,
  `iTime` bigint(20) DEFAULT NULL,
  `sProtocol` varchar(255) DEFAULT NULL ,
  `sSrcAddr` varchar(255) DEFAULT NULL ,
  `iSrcPort` int(11) DEFAULT NULL,
  `sSrcHostName` varchar(255) DEFAULT NULL,
  `sDesAddr` varchar(255) DEFAULT NULL ,
  `iDesPort` int(11) DEFAULT NULL,
  `iDisconnectTime` bigint(20) DEFAULT NULL ,
  `sUserName` varchar(255) DEFAULT NULL ,
  `iDataFlow` bigint(20) DEFAULT NULL ,
  `sCommand` varchar(255) DEFAULT NULL ,
  `iThreaten` int(11) DEFAULT NULL ,
  `sStatus` varchar(255) DEFAULT NULL ,
  `sDetail` text,
  PRIMARY KEY (`iId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_app_admin
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_app_admin`;
CREATE TABLE `m_tblog_app_admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sAppName` varchar(128) NOT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sProtocol` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sAction` varchar(64) NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTimeAppName` (`iTime`,`sAppName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_ddos
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_ddos`;
CREATE TABLE `m_tblog_ddos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sEventName` varchar(128) NOT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sThreshold` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sStatus` tinyint(2) NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTimeEventName` (`iTime`,`sEventName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_ddos_record
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_ddos_record`;
CREATE TABLE `m_tblog_ddos_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sEventName` varchar(64) NOT NULL ,
  `iCount` bigint(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sEventName` (`sEventName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblog_evil_code
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_evil_code`;
CREATE TABLE `m_tblog_evil_code` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sViruesName` varchar(128) NOT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sProtocol` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sStatus` varchar(64) NOT NULL ,
  `sLogLevel` varchar(64) DEFAULT NULL,
  `sFileName` varchar(256) DEFAULT NULL ,
  `sUserName` varchar(64) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTiemVirName` (`iTime`,`sViruesName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_evilcode_record
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_evilcode_record`;
CREATE TABLE `m_tblog_evilcode_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sVirusName` varchar(128) NOT NULL,
  `sLogLevel` varchar(64) DEFAULT NULL,
  `iCount` bigint(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sVirusName` (`sVirusName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblog_firewall
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_firewall`;
CREATE TABLE `m_tblog_firewall` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sInputPort` varchar(128) DEFAULT NULL ,
  `sOutPort` varchar(128) DEFAULT NULL ,
  `sSourceAddr` varchar(64) NOT NULL ,
  `sSourcePort` varchar(32) DEFAULT NULL ,
  `sProtocol` varchar(64) DEFAULT NULL ,
  `sTargetAddr` varchar(64) NOT NULL ,
  `sTargetPort` varchar(32) DEFAULT NULL ,
  `sAction` varchar(32) NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_TimeSipDip` (`iTime`,`sSourceAddr`,`sTargetAddr`),
  KEY `i_sourceip` (`sSourceAddr`,`iTime`) USING BTREE,
  KEY `i_targetip` (`sTargetAddr`,`iTime`) USING BTREE,
  KEY `i_action` (`sAction`,`iTime`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_info_leak
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_info_leak`;
CREATE TABLE `m_tblog_info_leak` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sFileKeywork` varchar(128) DEFAULT NULL ,
  `sFilterType` varchar(64) DEFAULT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sProtocol` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sStatus` varchar(64) NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTime` (`iTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_ips
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_ips`;
CREATE TABLE `m_tblog_ips` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sEventName` varchar(256) NOT NULL ,
  `sSourceIP` varchar(64) NOT NULL ,
  `sProtocol` varchar(64) NOT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sStatus` varchar(16) NOT NULL ,
  `sLogName` varchar(255) DEFAULT NULL ,
  `sRuleID` varchar(128) NOT NULL ,
  `sGrade` varchar(16) DEFAULT NULL ,
  `sDesc` varchar(256) DEFAULT NULL ,
  `sRuleType` varchar(256) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTimeAndEvent` (`iTime`,`sEventName`) USING BTREE,
  KEY `I_sRuleID` (`sRuleID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_ips_record
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_ips_record`;
CREATE TABLE `m_tblog_ips_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sEventName` varchar(256) NOT NULL ,
  `sRuleID` varchar(128) NOT NULL ,
  `sGrade` varchar(16) DEFAULT NULL ,
  `iCount` bigint(32) NOT NULL,
  `sRuleType` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sEventName` (`sEventName`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblog_library
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_library`;
CREATE TABLE `m_tblog_library` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sDate` varchar(32) NOT NULL,
  `sFileName` varchar(64) NOT NULL,
  `sSize` varchar(64) NOT NULL,
  `iTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for m_tblog_size_record
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_size_record`;
CREATE TABLE `m_tblog_size_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sLogName` varchar(255) NOT NULL,
  `sImportSize` bigint(32) NOT NULL DEFAULT '0',
  `iTime` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `log_name` (`sLogName`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblog_sys_admin
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_sys_admin`;
CREATE TABLE `m_tblog_sys_admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iUserId` varchar(50) NOT NULL ,
  `sSubAccount` varchar(64) DEFAULT NULL ,
  `iLoginTime` int(11) NOT NULL ,
  `sIp` varchar(64) DEFAULT NULL ,
  `sStatus` tinyint(2) NOT NULL ,
  `sContent` varchar(255) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_sys_backup
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_sys_backup`;
CREATE TABLE `m_tblog_sys_backup` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iUserId` varchar(50) NOT NULL ,
  `iLoginTime` int(11) NOT NULL ,
  `sIp` varchar(64) DEFAULT NULL ,
  `sStatus` tinyint(2) NOT NULL ,
  `sContent` varchar(255) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iLoginTime` (`iLoginTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_sys_reboot
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_sys_reboot`;
CREATE TABLE `m_tblog_sys_reboot` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iUserId` varchar(50) NOT NULL ,
  `iLoginTime` int(11) NOT NULL ,
  `sIp` varchar(64) DEFAULT NULL ,
  `sStatus` tinyint(2) NOT NULL ,
  `sContent` varchar(255) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iLoginTime` (`iLoginTime`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_sys_resource
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_sys_resource`;
CREATE TABLE `m_tblog_sys_resource` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sSubject` varchar(128) DEFAULT NULL ,
  `sContent` varchar(255) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_url_visit
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_url_visit`;
CREATE TABLE `m_tblog_url_visit` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(100) NOT NULL ,
  `sUrl` varchar(512) NOT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sWebType` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sAction` tinyint(2) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTime` (`iTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_webapp_record
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_webapp_record`;
CREATE TABLE `m_tblog_webapp_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sEventName` varchar(128) DEFAULT NULL ,
  `sSeverity` varchar(50) DEFAULT NULL,
  `sBugType` varchar(64) DEFAULT NULL ,
  `iCount` bigint(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sEventName` (`sEventName`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblog_webapplication
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_webapplication`;
CREATE TABLE `m_tblog_webapplication` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sEventName` varchar(128) DEFAULT NULL ,
  `sSourceIP` varchar(64) DEFAULT NULL ,
  `sBugType` varchar(64) DEFAULT NULL ,
  `sTargetIP` varchar(64) DEFAULT NULL ,
  `sStatus` varchar(10) DEFAULT NULL ,
  `sSeverity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `iTime` (`iTime`,`sEventName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tblog_wifi_audit
-- ----------------------------
DROP TABLE IF EXISTS `m_tblog_wifi_audit`;
CREATE TABLE `m_tblog_wifi_audit` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) NOT NULL ,
  `sShareHost` varchar(128) NOT NULL ,
  `sTerminal` varchar(512) DEFAULT NULL ,
  `sTableName` varchar(32) NOT NULL ,
  PRIMARY KEY (`id`),
  KEY `I_iTimeShareHost` (`iTime`,`sShareHost`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tbloginlog
-- ----------------------------
DROP TABLE IF EXISTS `m_tbloginlog`;
CREATE TABLE `m_tbloginlog` (
  `iloginLogId` bigint(20) NOT NULL AUTO_INCREMENT,
  `iUserId` varchar(50) NOT NULL,
  `iLoginTime` int(11) NOT NULL,
  `sIp` varchar(64) DEFAULT NULL,
  `sStatus` tinyint(2) NOT NULL,
  `sContent` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`iloginLogId`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tblogtable
-- ----------------------------
DROP TABLE IF EXISTS `m_tblogtable`;
CREATE TABLE `m_tblogtable` (
  `iId` bigint(20) NOT NULL AUTO_INCREMENT,
  `iLogtablename` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `iLogtablestate` varchar(2) CHARACTER SET utf8 DEFAULT '0',
  PRIMARY KEY (`iId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for m_tboperatelog
-- ----------------------------
DROP TABLE IF EXISTS `m_tboperatelog`;
CREATE TABLE `m_tboperatelog` (
  `iLogId` bigint(20) NOT NULL AUTO_INCREMENT,
  `iDateTime` int(11) NOT NULL,
  `sIp` varchar(64) NOT NULL,
  `sOperateUser` varchar(50) NOT NULL,
  `sRs` varchar(200) NOT NULL,
  `sContent` varchar(255) NOT NULL,
  `sOperateAction` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`iLogId`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tbprotected_log
-- ----------------------------
DROP TABLE IF EXISTS `m_tbprotected_log`;
CREATE TABLE `m_tbprotected_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) DEFAULT NULL ,
  `sScanType` varchar(64) DEFAULT NULL ,
  `sSourceAddr` varchar(64) DEFAULT NULL ,
  `sTargetAddr` varchar(64) DEFAULT NULL ,
  `iConnectNum` varchar(64) DEFAULT NULL ,
  `iAddressNum` varchar(64) DEFAULT NULL ,
  `iPortNum` varchar(64) DEFAULT NULL ,
  `iPortRange` varchar(64) DEFAULT NULL ,
  `sDetail` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tbrevcamera_log
-- ----------------------------
DROP TABLE IF EXISTS `m_tbrevcamera_log`;
CREATE TABLE `m_tbrevcamera_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iTime` int(11) DEFAULT NULL ,
  `sTrigerReason` varchar(512) DEFAULT NULL ,
  `sTargetAddr` varchar(64) DEFAULT NULL ,
  `sHostType` varchar(128) DEFAULT NULL ,
  `sDistance` varchar(64) DEFAULT NULL ,
  `sTimeDelay` varchar(64) DEFAULT NULL ,
  `sDetail` text ,
  `sFileName` varchar(512) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 CHECKSUM=1 ;

-- ----------------------------
-- Table structure for m_tbstatistics
-- ----------------------------
DROP TABLE IF EXISTS `m_tbstatistics`;
CREATE TABLE `m_tbstatistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sName` varchar(128) DEFAULT NULL ,
  `sValue` text ,
  `sMark` varchar(512) DEFAULT NULL ,
  PRIMARY KEY (`id`),
  UNIQUE KEY `i_name` (`sName`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;

-- ----------------------------
-- Table structure for m_tbsystem_update_log
-- ----------------------------
DROP TABLE IF EXISTS `m_tbsystem_update_log`;
CREATE TABLE `m_tbsystem_update_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sVersion` varchar(128) DEFAULT NULL ,
  `sDescription` varchar(512) DEFAULT NULL ,
  `iTime` int(11) DEFAULT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for m_tbwebapplication_lib
-- ----------------------------
DROP TABLE IF EXISTS `m_tbwebapplication_lib`;
CREATE TABLE `m_tbwebapplication_lib` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sRuleID` varchar(128) DEFAULT NULL ,
  `sRealID` varchar(128) DEFAULT NULL ,
  `iPriority` tinyint(2) DEFAULT NULL ,
  `sRuleName` varchar(512) DEFAULT NULL ,
  `sDesc` text ,
  `sType` varchar(128) DEFAULT NULL ,
  `sDangerLever` varchar(64) DEFAULT NULL ,
  `sInterceptionMethod` varchar(64) DEFAULT NULL ,
  `sHttpRequestType` varchar(64) DEFAULT NULL ,
  `sMatchAlgorithm` varchar(64) DEFAULT NULL ,
  `sMatchContent` varchar(64) DEFAULT NULL ,
  `sFeatureKey` varchar(512) DEFAULT NULL ,
  `iStatus` tinyint(2) DEFAULT NULL ,
  `iUpdateTime` int(11) DEFAULT NULL ,
  `iCustomOrInset` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;
