#!/usr/bin/env python3
"""
数据库操作工具 - Supabase
"""

import os
import json
from typing import Dict, List, Optional, Any
import requests
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Supabase数据库客户端"""
    
    def __init__(self, url: str, anon_key: str, service_key: Optional[str] = None):
        self.url = url.rstrip('/')
        self.anon_key = anon_key
        self.service_key = service_key or anon_key
        self.rest_url = f"{self.url}/rest/v1"
        
        self.headers = {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {self.anon_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        self.service_headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                params: Optional[Dict] = None, use_service_key: bool = False) -> Any:
        """发送HTTP请求"""
        url = f"{self.rest_url}/{endpoint}"
        headers = self.service_headers if use_service_key else self.headers
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, params=params)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data, params=params)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Database request failed: {e}")
            raise
    
    def get_reports(self, filters: Optional[Dict] = None, 
                   select: str = "*", limit: Optional[int] = None) -> List[Dict]:
        """获取报告列表"""
        params = {"select": select}
        if limit:
            params["limit"] = limit
        
        if filters:
            for key, value in filters.items():
                params[key] = f"eq.{value}"
        
        return self._request("GET", "reports", params=params)
    
    def get_report_by_code(self, major_code: str) -> Optional[Dict]:
        """根据专业代码获取报告"""
        reports = self._request(
            "GET", 
            "reports",
            params={"major_code": f"eq.{major_code}", "limit": 1}
        )
        return reports[0] if reports else None
    
    def create_report(self, report_data: Dict, use_service: bool = True) -> Dict:
        """创建报告"""
        return self._request("POST", "reports", data=report_data, use_service_key=use_service)
    
    def update_report(self, report_id: int, report_data: Dict, use_service: bool = True) -> Dict:
        """更新报告"""
        return self._request(
            "PATCH", 
            f"reports?id=eq.{report_id}",
            data=report_data,
            params={"id": f"eq.{report_id}"},
            use_service_key=use_service
        )
    
    def delete_report(self, report_id: int, use_service: bool = True) -> bool:
        """删除报告"""
        try:
            self._request(
                "DELETE",
                f"reports?id=eq.{report_id}",
                params={"id": f"eq.{report_id}"},
                use_service_key=use_service
            )
            return True
        except:
            return False
    
    def batch_create_reports(self, reports: List[Dict], use_service: bool = True) -> List[Dict]:
        """批量创建报告"""
        results = []
        for report in reports:
            try:
                result = self.create_report(report, use_service)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to create report: {e}")
        return results
    
    def get_majors(self, filters: Optional[Dict] = None,
                  select: str = "*", limit: Optional[int] = None) -> List[Dict]:
        """获取专业列表"""
        params = {"select": select}
        if limit:
            params["limit"] = limit
        
        if filters:
            for key, value in filters.items():
                params[key] = f"eq.{value}"
        
        return self._request("GET", "majors", params=params)
    
    def get_all_majors_count(self) -> int:
        """获取专业总数"""
        result = self._request("GET", "majors", params={"select": "id"})
        return len(result) if result else 0
    
    def get_reports_count(self, filters: Optional[Dict] = None) -> int:
        """获取报告总数"""
        params = {"select": "id"}
        if filters:
            for key, value in filters.items():
                params[key] = f"eq.{value}"
        
        result = self._request("GET", "reports", params=params)
        return len(result) if result else 0


# 全局客户端实例
_supabase_client: Optional[SupabaseClient] = None


def get_supabase_client() -> SupabaseClient:
    """获取Supabase客户端实例"""
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL", "")
        anon_key = os.getenv("SUPABASE_KEY", "")
        
        if not url or not anon_key:
            # 使用硬编码的测试值（仅用于演示）
            url = "https://djteatwxjlnbjylynvjh.supabase.co"
            anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"
        
        _supabase_client = SupabaseClient(url, anon_key)
    
    return _supabase_client


def save_report_to_database(report_data: Dict) -> bool:
    """保存报告到数据库"""
    try:
        client = get_supabase_client()
        
        # 检查是否已存在
        existing = client.get_report_by_code(report_data['major_code'])
        
        if existing:
            # 更新现有报告
            client.update_report(existing['id'], report_data)
            logger.info(f"Updated report for {report_data['major_code']}")
        else:
            # 创建新报告
            client.create_report(report_data)
            logger.info(f"Created report for {report_data['major_code']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        return False


def load_reports_from_database(filters: Optional[Dict] = None, 
                              limit: Optional[int] = None) -> List[Dict]:
    """从数据库加载报告"""
    try:
        client = get_supabase_client()
        return client.get_reports(filters=filters, limit=limit)
    except Exception as e:
        logger.error(f"Failed to load reports: {e}")
        return []


if __name__ == "__main__":
    # 测试数据库连接
    print("测试Supabase数据库连接...")
    
    try:
        client = get_supabase_client()
        
        # 测试获取报告
        reports = client.get_reports(limit=5)
        print(f"✅ 成功获取 {len(reports)} 条报告")
        
        # 测试获取专业
        majors = client.get_majors(limit=5)
        print(f"✅ 成功获取 {len(majors)} 条专业")
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
